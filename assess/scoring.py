"""Current-state analysis: TIME classification, legacy risk, integration
complexity and maturity gaps (current state vs target state)."""
from collections import Counter
from dataclasses import dataclass

from assess.inventory import Application, Integration


def time_category(app: Application) -> str:
    """Gartner TIME model: business value x technical health.
    Invest = keep and develop, Migrate = valuable but technically weak,
    Tolerate = works but low value, Eliminate = retire."""
    valuable = app.business_value >= 3
    healthy = app.technical_health >= 3
    if valuable and healthy:
        return "Invest"
    if valuable:
        return "Migrate"
    if healthy:
        return "Tolerate"
    return "Eliminate"


def legacy_risk(app: Application) -> tuple[int, list[str]]:
    """0-10 score with the reasons, so the finding is explainable to a client."""
    score, reasons = 0, []
    if app.vendor_support == "no":
        score, reasons = score + 3, reasons + ["no vendor support"]
    elif app.vendor_support == "ending":
        score, reasons = score + 2, reasons + ["vendor support ending"]
    if app.age_years >= 10:
        score, reasons = score + 2, reasons + [f"{app.age_years} years old"]
    if app.technical_health <= 2:
        score, reasons = score + 2, reasons + ["poor technical health"]
    if app.hosting == "on-prem":
        score, reasons = score + 1, reasons + ["on-prem infrastructure"]
    if app.hosting == "end-user":
        score, reasons = score + 2, reasons + ["end-user computing (spreadsheet)"]
    return min(score, 10), reasons


@dataclass
class IntegrationSummary:
    total: int
    by_method: dict[str, int]
    point_to_point: int          # every link that is not a managed API
    manual: list[Integration]
    degree: dict[str, int]       # links per application
    hubs: list[str]              # apps that many others depend on


def analyze_integrations(links: list[Integration], hub_threshold: int = 4) -> IntegrationSummary:
    degree = Counter()
    for link in links:
        degree[link.source] += 1
        degree[link.target] += 1
    methods = Counter(link.method for link in links)
    return IntegrationSummary(
        total=len(links),
        by_method=dict(methods),
        point_to_point=len(links) - methods.get("api", 0),
        manual=[l for l in links if l.method == "manual"],
        degree=dict(degree),
        hubs=sorted(a for a, d in degree.items() if d >= hub_threshold),
    )


def maturity_gaps(maturity: dict[str, dict]) -> list[tuple[str, int, int, int]]:
    """(dimension, current, target, gap), biggest gap first."""
    rows = [(dim, d["current"], d["target"], d["target"] - d["current"])
            for dim, d in maturity.items()]
    return sorted(rows, key=lambda r: (-r[3], r[0]))
