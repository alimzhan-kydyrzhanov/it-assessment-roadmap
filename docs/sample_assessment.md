# IT Current-State Assessment and Roadmap — Riverside Clinic Group (synthetic)

## Executive summary

- 12 applications, EUR 682,000 annual run cost, 7 of 12 on-prem.
- TIME: 6 Invest, 4 Migrate, 1 Tolerate, 1 Eliminate.
- 11 of 13 integrations are point-to-point, 3 are manual.
- Largest maturity gap: Integrations (1 -> 4).
- Roadmap: 13 initiatives in 4 waves.

## Application portfolio (TIME)

| App | Domain | Value | Health | TIME | Legacy risk |
| --- | --- | --- | --- | --- | --- |
| StockTrack Inventory | Operations | 2 | 2 | Eliminate | 7/10 |
| LabLink | Clinical | 4 | 3 | Invest | 1/10 |
| PACS Imaging | Clinical | 5 | 4 | Invest | 0/10 |
| Patient Portal | Patient Access | 4 | 4 | Invest | 0/10 |
| FinCore ERP | Finance | 5 | 3 | Invest | 3/10 |
| PayrollPlus | HR | 3 | 4 | Invest | 0/10 |
| BI Reporting | Analytics | 4 | 3 | Invest | 0/10 |
| MedRecord EHR | Clinical | 5 | 2 | Migrate | 7/10 |
| BookIt Scheduling | Patient Access | 4 | 2 | Migrate | 8/10 |
| Excel Billing Macros | Finance | 3 | 1 | Migrate | 7/10 |
| Doctor Rota Tool | Operations | 3 | 2 | Migrate | 8/10 |
| HR Docs Share | HR | 1 | 3 | Tolerate | 1/10 |

## Top legacy risks

- **BookIt Scheduling** (8/10): no vendor support, 12 years old, poor technical health, on-prem infrastructure
- **Doctor Rota Tool** (8/10): no vendor support, 10 years old, poor technical health, on-prem infrastructure
- **MedRecord EHR** (7/10): vendor support ending, 14 years old, poor technical health, on-prem infrastructure
- **Excel Billing Macros** (7/10): no vendor support, poor technical health, end-user computing (spreadsheet)
- **StockTrack Inventory** (7/10): vendor support ending, 13 years old, poor technical health, on-prem infrastructure

## Integrations

Methods: api 2, db-link 3, file 5, manual 3. Hubs (4+ links): MedRecord EHR, BookIt Scheduling, FinCore ERP.

## Maturity: current vs target

| Dimension | Current | Target | Gap |
| --- | --- | --- | --- |
| Integrations | 1 | 4 | 3 |
| Architecture | 2 | 4 | 2 |
| Infrastructure | 2 | 4 | 2 |
| Data & Analytics | 2 | 3 | 1 |
| Operating Model | 2 | 3 | 1 |
| Security & Compliance | 3 | 4 | 1 |

## Roadmap

| Wave | Initiative | Why | Value | Effort | Depends on |
| --- | --- | --- | --- | --- | --- |
| Wave 1 (0-3 months) | Automate manual interface Excel Billing Macros -> FinCore ERP | manual weekly data transfer, error-prone | 3 | 1 | - |
| Wave 1 (0-3 months) | Automate manual interface Doctor Rota Tool -> BookIt Scheduling | manual daily data transfer, error-prone | 3 | 1 | - |
| Wave 1 (0-3 months) | Retire StockTrack Inventory | low value and poor health, saves EUR 9,000/year | 2 | 1 | - |
| Wave 1 (0-3 months) | Move reporting off production databases to a data warehouse | Data & Analytics maturity 2 -> 3 | 3 | 2 | - |
| Wave 1 (0-3 months) | Move from ticket-based IT to product teams with business owners | Operating Model maturity 2 -> 3 | 3 | 2 | - |
| Wave 1 (0-3 months) | Add audit logging and access reviews for patient data systems | Security & Compliance maturity 3 -> 4 | 3 | 2 | - |
| Wave 2 (3-6 months) | Set up architecture principles, standards and a review board | Architecture maturity 2 -> 4 | 4 | 3 | - |
| Wave 2 (3-6 months) | Define a cloud / hosting strategy and a landing zone | Infrastructure maturity 2 -> 4 | 4 | 3 | - |
| Wave 2 (3-6 months) | Modernize or replace Excel Billing Macros | high business value (3) but health 1 | 3 | 3 | - |
| Wave 2 (3-6 months) | Modernize or replace Doctor Rota Tool | high business value (3) but health 2 | 3 | 3 | - |
| Wave 3 (6-12 months) | Introduce an integration layer (APIs) for core systems | 11 of 13 integrations are point-to-point; hubs: MedRecord EHR, BookIt Scheduling, FinCore ERP | 5 | 4 | - |
| Wave 4 (12+ months) | Modernize or replace BookIt Scheduling | high business value (4) but health 2 | 4 | 3 | INT-PLATFORM |
| Wave 4 (12+ months) | Modernize or replace MedRecord EHR | high business value (5) but health 2 | 5 | 5 | INT-PLATFORM |
