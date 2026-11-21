# IT Current-State Assessment & Transformation Roadmap

A small Python toolkit for the core of a technology strategy engagement:
**assess the current state of an IT landscape against a target state and turn
the gaps into a phased roadmap.** The data is a synthetic clinic group
(12 applications, 13 integrations, 6 maturity dimensions).

```
applications.csv ─┐
integrations.csv ─┼─> analysis ─────────────> initiatives ──> roadmap waves ──> report (Markdown + JSON)
maturity.json ────┘   TIME, legacy risk,       value/effort,    dependency
                      integration complexity,  dependencies     order
                      maturity gaps
```

## What it does
- **Application portfolio (TIME model):** classifies each application as Tolerate, Invest,
  Migrate or Eliminate from business value and technical health.
- **Legacy risk score (0-10) with reasons:** vendor support, age, health, on-prem, spreadsheets.
- **Integration analysis:** point-to-point vs API links, manual interfaces, hub systems.
- **Maturity gaps:** current vs target level for architecture, infrastructure, integrations,
  data, security and operating model.
- **Roadmap:** initiatives with value, effort and dependencies, placed in waves
  (0-3, 3-6, 6-12, 12+ months) in dependency order; dependency cycles are rejected.

See the output in [`docs/sample_assessment.md`](docs/sample_assessment.md).

## Run
```bash
pip install -r requirements.txt
pytest -v
python -m assess.cli --data data --out reports/assessment.md
```
Docker: `docker build -t it-assessment . && docker run --rm it-assessment`

## Limitations (honest)
- Scores in the input files come from interviews in a real engagement; here they are synthetic.
- The rules that turn findings into initiatives are simple and transparent on purpose.
  A real roadmap is agreed with client stakeholders, not generated.
- No cost model (business case, TCO) beyond the annual run cost.
