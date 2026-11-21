from pathlib import Path

import pytest

from assess.cli import run
from assess.inventory import Application, Integration, load_applications
from assess.roadmap import Initiative, plan_waves
from assess.scoring import analyze_integrations, legacy_risk, maturity_gaps, time_category

DATA = Path(__file__).parent.parent / "data"


def app(value, health, **kw):
    base = dict(app_id="X", name="X", domain="D", business_value=value, technical_health=health,
                annual_cost_eur=0, users=1, hosting="saas", vendor_support="yes", age_years=1)
    return Application(**{**base, **kw})


@pytest.mark.parametrize("value,health,expected", [
    (5, 5, "Invest"), (4, 2, "Migrate"), (2, 4, "Tolerate"), (1, 1, "Eliminate"),
    (3, 3, "Invest"),  # boundary: 3 counts as high
])
def test_time_quadrants(value, health, expected):
    assert time_category(app(value, health)) == expected


def test_legacy_risk_explains_itself():
    score, reasons = legacy_risk(app(5, 2, hosting="on-prem", vendor_support="no", age_years=12))
    assert score == 8
    assert "no vendor support" in reasons and "12 years old" in reasons


def test_integration_hubs_and_point_to_point():
    links = [Integration("A", t, "file", "daily") for t in "BCDE"] + [Integration("B", "C", "api", "rt")]
    s = analyze_integrations(links)
    assert s.point_to_point == 4 and s.hubs == ["A"]


def test_maturity_gaps_sorted_biggest_first():
    gaps = maturity_gaps({"A": {"current": 3, "target": 4}, "B": {"current": 1, "target": 4}})
    assert gaps[0] == ("B", 1, 4, 3)


def test_waves_respect_dependencies():
    items = [Initiative("BASE", "b", "", 5, 4), Initiative("QUICK", "q", "", 3, 1, ["BASE"])]
    planned = {i.key: i.wave for i in plan_waves(items)}
    assert planned["QUICK"] > planned["BASE"]


def test_dependency_cycle_is_rejected():
    items = [Initiative("A", "a", "", 1, 1, ["B"]), Initiative("B", "b", "", 1, 1, ["A"])]
    with pytest.raises(ValueError, match="cycle"):
        plan_waves(items)


def test_invalid_score_is_rejected(tmp_path):
    bad = (DATA / "applications.csv").read_text().replace("A01,MedRecord EHR,Clinical,5", "A01,MedRecord EHR,Clinical,9")
    path = tmp_path / "apps.csv"
    path.write_text(bad)
    with pytest.raises(ValueError, match="1-5"):
        load_applications(path)


def test_end_to_end_report(tmp_path):
    roadmap = run(str(DATA), str(tmp_path / "a.md"), "Test")
    text = (tmp_path / "a.md").read_text()
    keys = {i.key for i in roadmap}
    assert "INT-PLATFORM" in keys and "MOD-A01" in keys and "RET-A09" in keys
    mod = next(i for i in roadmap if i.key == "MOD-A01")
    assert "INT-PLATFORM" in mod.depends_on and mod.wave == 4
    assert "AUTO-A09-A06" not in keys     # retired app: no automation
    assert "## Roadmap" in text and "Executive summary" in text
    assert (tmp_path / "a.json").exists()
