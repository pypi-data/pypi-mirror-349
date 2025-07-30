# nimmunize

> **Nigeria immunisation scheduling & survey‑analytics toolkit**
> Offline‑ready • FHIR‑friendly • GPL‑3

![NPHCDA poster](https://pbs.twimg.com/media/GfEsdOzXAAEVi69?format=jpg\&name=large)

`nimmunize` turns Nigeria’s routine‑immunisation schedule into a **library** and a set of **command‑line tools** 

---

## What it does — in one glance

| Layer                                     | Capability                                                                                                                                                                                                               | Key APIs / CLI                                                                             |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| **Schedule engine**                       | • Calculate **next-due dose** with *volume*, *route* & *diseases prevented*.<br>• Flag **overdue series** and number of days late.<br>• Surface rich **poster metadata** (`title`, `url`, `image_url`) for audit trails. | `next_due()` • `overdue()` • `reference()`                                                 |
| **Survey analytics**                      | • **Bulk-audit** CSV/Excel exports.<br>• Compute *coverage %*, *FIC*, **route-level** coverage & **disease-level** protection.<br>• Produce **defaulter lists** & “Fully immunised” rosters.                             | `nimmunize survey …` • `audit()` • `metrics()` • `route_coverage()` • `disease_coverage()` |
| **Catch-up planner**                      | Generate **safe catch-up schedules** that respect minimum ages & intervals (WHO algorithm).                                                                                                                              | `catchup_plan()` • `nimmunize catchup …` *(coming soon)*                                   |




---




## Installation Installation

```bash
pip install nimmunize            # Python ≥ 3.9
```


Need dev extras? `pip install nimmunize[dev]` to get `pytest`, `black`, and pre‑commit hooks.

---

## 🚀 Quick start

### 1 · Library usage

```python
from datetime import date
from nimmunize import next_due, overdue, disease_coverage

# Child record
child_dob = date(2024, 7, 15)
shots_taken = {"bcg": child_dob, "opv": [child_dob]}  # BCG + OPV0 at birth

# 1️⃣ Compute next doses (simple dictionary)
print(next_due(child_dob, shots_taken))

# 2️⃣ Same but ask for deep details (dosage / route / diseases)
print(next_due(child_dob, shots_taken, include_details=True)["opv"])

# 3️⃣ Were we late by 1 January 2025?
print(overdue(child_dob, shots_taken, as_of=date(2025, 1, 1)))
```

### 2 · Survey workflow

```python
import nimmunize as ni

survey_df   = ni.load("baseline_clusters.xlsx")  # any .csv/.xls/.xlsx or DataFrame
annotated   = ni.audit(survey_df)                # adds missed_/delay_/next_due_ cols
print(ni.metrics(annotated))                     # {'coverage_%': …, 'FIC_%': …}
print(ni.route_coverage(annotated))              # {'Intramuscular': 88.4, 'Oral': 91.2, …}
print(ni.disease_coverage(annotated))            # {'polio': 89.6, 'measles': 82.3, …}
print("⚠️ Diseases <80 % protected:", ni.diseases_at_risk(annotated))
```

### 3 · CLI in two commands

```bash
# Bulk annotate a survey and print coverage dashboard
nimmunize survey data/cluster.csv -o cluster_audited.csv

# One‑off JSON catch‑up (verbose output)
nimmunize nextdose 2019-04-12 -t pentavalent 2019-10-27 -t opv 2019-10-27 --as-of 2025-05-01 --details
```

Run `nimmunize --help` for the full option tree.

---

## Essentials

```python
# SCHEDULING
next_due(dob, taken, *, as_of=None, include_details=False) -> {ag: date|dict}
overdue(dob, taken, *, as_of=None) -> {missed_<ag>, delay_<ag>}
reference() -> {'title', 'published', 'url', 'image_url'}

# SURVEY
load(path|DF, *, dob_col='dob') -> DataFrame
audit(df, *, as_of=None) -> DataFrame
metrics(df) -> {'coverage_%', 'FIC_%'}
route_coverage(df) -> {route: %}
disease_coverage(df) -> {disease: %}
diseases_at_risk(df, threshold=80) -> [disease]

# CATCH‑UP\ ncatchup_plan(dob, taken, *, as_of=None) -> {ag: [dates]}
```

All objects are plain Python & pandas—easy to feed into Streamlit, FastAPI, or Jupyter notebooks.

---


---

## 🗺️ Road‑map (public backlog)

* [x] Detailed schedule with route & disease metadata.
* [x] Disease‑level coverage & risk flags.
* [ ] CLI catch‑up planner (`nimmunize catchup`).
* [ ] Dash mini‑dashboard.
* [ ] `nimmunizeR` wrapper for the Stata/epi community.


Love a feature? [Open an issue](https://github.com/yourusername/nimmunize/issues) or up‑vote existing ones.

---

## 🧪 Contributing & dev setup

```bash
# After forking the repo
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]          # pytest, black, pre‑commit, isort, mypy
pre-commit install             # automatic lint on every git commit
pytest -q                      # run fast unit tests ✨
```

1. **Branch** off `main` → commit logically → open a **PR**.
2. Ensure `pytest` & `flake8` pass.
3. Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

##  Data sources & license

* Schedule data © NPHCDA Immunization Schedule (18 Dec 2024)
* Code licensed under **GNU GPL v3**—see `LICENSE`.
* By using the library you agree to verify clinical decisions with qualified healthcare professionals. No warranty.
