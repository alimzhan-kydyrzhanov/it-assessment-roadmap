"""Load and validate the current-state inputs: application inventory,
integrations and the IT maturity assessment."""
import csv
import json
from dataclasses import dataclass
from pathlib import Path

HOSTING = {"on-prem", "private-cloud", "saas", "end-user"}
SUPPORT = {"yes", "ending", "no"}
METHODS = {"api", "file", "db-link", "manual"}


@dataclass(frozen=True)
class Application:
    app_id: str
    name: str
    domain: str
    business_value: int      # 1-5, from business interviews
    technical_health: int    # 1-5, from IT interviews and documentation
    annual_cost_eur: float
    users: int
    hosting: str
    vendor_support: str
    age_years: int


@dataclass(frozen=True)
class Integration:
    source: str
    target: str
    method: str
    frequency: str


def _score(value: str, field: str, row: int) -> int:
    number = int(value)
    if not 1 <= number <= 5:
        raise ValueError(f"row {row}: {field} must be 1-5, got {number}")
    return number


def load_applications(path: str | Path) -> dict[str, Application]:
    apps = {}
    with open(path, newline="", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f), start=2):
            if r["app_id"] in apps:
                raise ValueError(f"row {i}: duplicate app_id {r['app_id']}")
            if r["hosting"] not in HOSTING or r["vendor_support"] not in SUPPORT:
                raise ValueError(f"row {i}: unknown hosting or vendor_support value")
            apps[r["app_id"]] = Application(
                r["app_id"], r["name"], r["domain"],
                _score(r["business_value"], "business_value", i),
                _score(r["technical_health"], "technical_health", i),
                float(r["annual_cost_eur"]), int(r["users"]),
                r["hosting"], r["vendor_support"], int(r["age_years"]),
            )
    return apps


def load_integrations(path: str | Path, apps: dict[str, Application]) -> list[Integration]:
    links = []
    with open(path, newline="", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f), start=2):
            if r["source"] not in apps or r["target"] not in apps:
                raise ValueError(f"row {i}: integration points to an unknown application")
            if r["method"] not in METHODS:
                raise ValueError(f"row {i}: unknown method {r['method']}")
            links.append(Integration(r["source"], r["target"], r["method"], r["frequency"]))
    return links


def load_maturity(path: str | Path) -> dict[str, dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for dim, d in data.items():
        if not (1 <= d["current"] <= 5 and 1 <= d["target"] <= 5):
            raise ValueError(f"{dim}: maturity levels must be 1-5")
    return data
