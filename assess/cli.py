"""python -m assess.cli --data data --out reports/assessment.md"""
import argparse
import json
from pathlib import Path

from assess.inventory import load_applications, load_integrations, load_maturity
from assess.report import render
from assess.roadmap import build_initiatives, plan_waves
from assess.scoring import analyze_integrations, maturity_gaps


def run(data_dir: str, out_path: str, org: str) -> list:
    d = Path(data_dir)
    apps = load_applications(d / "applications.csv")
    integ = analyze_integrations(load_integrations(d / "integrations.csv", apps))
    gaps = maturity_gaps(load_maturity(d / "maturity.json"))
    roadmap = plan_waves(build_initiatives(apps, integ, gaps))
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(apps, integ, gaps, roadmap, org), encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(
        [{**i.__dict__, "priority": i.priority} for i in roadmap], indent=2), encoding="utf-8")
    return roadmap


def main():
    p = argparse.ArgumentParser(description="IT current-state assessment and roadmap")
    p.add_argument("--data", default="data")
    p.add_argument("--out", default="reports/assessment.md")
    p.add_argument("--org", default="Riverside Clinic Group (synthetic)")
    a = p.parse_args()
    roadmap = run(a.data, a.out, a.org)
    print(f"{len(roadmap)} initiatives -> {a.out}")


if __name__ == "__main__":
    main()
