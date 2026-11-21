"""Markdown assessment report: what a client steering committee would read."""
from collections import Counter

from assess.inventory import Application
from assess.roadmap import WAVES, Initiative
from assess.scoring import IntegrationSummary, legacy_risk, time_category


def render(apps: dict[str, Application], integ: IntegrationSummary,
           gaps: list, roadmap: list[Initiative], org: str = "Client") -> str:
    cats = Counter(time_category(a) for a in apps.values())
    total_cost = sum(a.annual_cost_eur for a in apps.values())
    on_prem = sum(a.hosting == "on-prem" for a in apps.values())
    risky = sorted(((legacy_risk(a), a) for a in apps.values()),
                   key=lambda x: -x[0][0])[:5]
    biggest = gaps[0] if gaps else None

    out = [f"# IT Current-State Assessment and Roadmap — {org}", "",
           "## Executive summary", "",
           f"- {len(apps)} applications, EUR {total_cost:,.0f} annual run cost, "
           f"{on_prem} of {len(apps)} on-prem.",
           f"- TIME: {cats['Invest']} Invest, {cats['Migrate']} Migrate, "
           f"{cats['Tolerate']} Tolerate, {cats['Eliminate']} Eliminate.",
           f"- {integ.point_to_point} of {integ.total} integrations are point-to-point, "
           f"{len(integ.manual)} are manual.",
           ]
    if biggest:
        out.append(f"- Largest maturity gap: {biggest[0]} ({biggest[1]} -> {biggest[2]}).")
    out.append(f"- Roadmap: {len(roadmap)} initiatives in "
               f"{len({i.wave for i in roadmap})} waves.")

    out += ["", "## Application portfolio (TIME)", "",
            "| App | Domain | Value | Health | TIME | Legacy risk |",
            "| --- | --- | --- | --- | --- | --- |"]
    for a in sorted(apps.values(), key=lambda a: (time_category(a), a.app_id)):
        out.append(f"| {a.name} | {a.domain} | {a.business_value} | {a.technical_health} | "
                   f"{time_category(a)} | {legacy_risk(a)[0]}/10 |")

    out += ["", "## Top legacy risks", ""]
    out += [f"- **{a.name}** ({score}/10): {', '.join(reasons)}" for (score, reasons), a in risky]

    out += ["", "## Integrations", "",
            f"Methods: {', '.join(f'{m} {n}' for m, n in sorted(integ.by_method.items()))}. "
            f"Hubs (4+ links): {', '.join(apps[h].name for h in integ.hubs) or 'none'}."]

    out += ["", "## Maturity: current vs target", "",
            "| Dimension | Current | Target | Gap |", "| --- | --- | --- | --- |"]
    out += [f"| {d} | {c} | {t} | {g} |" for d, c, t, g in gaps]

    out += ["", "## Roadmap", "",
            "| Wave | Initiative | Why | Value | Effort | Depends on |",
            "| --- | --- | --- | --- | --- | --- |"]
    out += [f"| {WAVES[i.wave]} | {i.title} | {i.rationale} | {i.value} | {i.effort} | "
            f"{', '.join(i.depends_on) or '-'} |" for i in roadmap]
    return "\n".join(out) + "\n"
