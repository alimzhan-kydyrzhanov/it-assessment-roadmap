"""Turn findings into initiatives and a phased transformation roadmap.

Each initiative has value and effort (1-5) and dependencies. Waves respect
dependencies: an initiative never starts before what it depends on.
"""
from dataclasses import dataclass, field
from graphlib import CycleError, TopologicalSorter

from assess.inventory import Application
from assess.scoring import IntegrationSummary, time_category

WAVES = {1: "Wave 1 (0-3 months)", 2: "Wave 2 (3-6 months)",
         3: "Wave 3 (6-12 months)", 4: "Wave 4 (12+ months)"}

MATURITY_ACTIONS = {
    "Architecture": "Set up architecture principles, standards and a review board",
    "Infrastructure": "Define a cloud / hosting strategy and a landing zone",
    "Data & Analytics": "Move reporting off production databases to a data warehouse",
    "Security & Compliance": "Add audit logging and access reviews for patient data systems",
    "Operating Model": "Move from ticket-based IT to product teams with business owners",
}


@dataclass
class Initiative:
    key: str
    title: str
    rationale: str
    value: int
    effort: int
    depends_on: list[str] = field(default_factory=list)
    wave: int = 0

    @property
    def priority(self) -> float:
        return round(self.value / self.effort, 2)


def build_initiatives(apps: dict[str, Application], integ: IntegrationSummary,
                      gaps: list[tuple[str, int, int, int]]) -> list[Initiative]:
    items: list[Initiative] = []
    platform = None
    if integ.point_to_point >= 5:
        platform = Initiative(
            "INT-PLATFORM", "Introduce an integration layer (APIs) for core systems",
            f"{integ.point_to_point} of {integ.total} integrations are point-to-point; "
            f"hubs: {', '.join(apps[h].name for h in integ.hubs) or 'none'}", value=5, effort=4)
        items.append(platform)

    for link in integ.manual:
        if time_category(apps[link.source]) == "Eliminate":
            continue  # no point automating a feed from a system we retire
        items.append(Initiative(
            f"AUTO-{link.source}-{link.target}",
            f"Automate manual interface {apps[link.source].name} -> {apps[link.target].name}",
            f"manual {link.frequency} data transfer, error-prone", value=3, effort=1))

    for app in apps.values():
        category = time_category(app)
        coupled = integ.degree.get(app.app_id, 0) >= 3
        deps = [platform.key] if platform and coupled else []
        if category == "Migrate":
            effort = 5 if app.users > 200 or app.annual_cost_eur > 100000 else 3
            items.append(Initiative(
                f"MOD-{app.app_id}", f"Modernize or replace {app.name}",
                f"high business value ({app.business_value}) but health {app.technical_health}",
                value=app.business_value, effort=effort, depends_on=deps))
        elif category == "Eliminate":
            items.append(Initiative(
                f"RET-{app.app_id}", f"Retire {app.name}",
                f"low value and poor health, saves EUR {app.annual_cost_eur:,.0f}/year",
                value=2, effort=1, depends_on=deps))

    for dim, cur, tgt, gap in gaps:
        if gap >= 1 and dim in MATURITY_ACTIONS:
            items.append(Initiative(
                f"MAT-{dim.split()[0].upper()}", MATURITY_ACTIONS[dim],
                f"{dim} maturity {cur} -> {tgt}", value=min(5, 2 + gap), effort=2 + (gap > 1)))
    return items


def plan_waves(items: list[Initiative]) -> list[Initiative]:
    """Assign waves in dependency order; raise on a dependency cycle."""
    by_key = {i.key: i for i in items}
    graph = {i.key: set(i.depends_on) for i in items}
    for deps in graph.values():
        missing = deps - by_key.keys()
        if missing:
            raise ValueError(f"unknown dependency {missing}")
    try:
        order = list(TopologicalSorter(graph).static_order())
    except CycleError as err:
        raise ValueError(f"dependency cycle: {err.args[1]}") from err
    for key in order:
        item = by_key[key]
        base = 1 if item.effort <= 2 else 2 if item.effort <= 3 else 3
        after = max((by_key[d].wave + 1 for d in item.depends_on), default=1)
        item.wave = min(4, max(base, after))
    return sorted(items, key=lambda i: (i.wave, -i.priority, i.key))
