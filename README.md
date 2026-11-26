# Sequential state-of-charge laboratory — IJOTIS revision

**Release candidate for author review.** Do not publish until the corresponding author approves data/code distribution and licensing. This package accompanies *A Proposed Undergraduate Engineering Laboratory Framework for Sequential State-of-Charge Estimation Using No-Load Electric Vehicle Data*. It is not an implemented or validated educational intervention.

## Contents
- `data/ev_log.csv`: 7,323 records from the supplied Excel log, with four trailing empty rows omitted and headers standardized; no synthetic observations or altered measured values.
- `analysis.py`: reproducible chronological analysis, five delta predictors, direct comparison of three original models, expanding-window evaluation and color figures.
- `solution_notebook.ipynb`: executable instructor solution with explanatory cells.
- `student_worksheet.md` and `instructor_guide.md`: proposed two-session activity and analytic rubric.
- `results/`: metrics, predictions and figures used in the revised manuscript.

## Run
Python 3 in a clean environment from the repository root:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python analysis.py
jupyter notebook solution_notebook.ipynb
```
The script overwrites result files in `results/`. Expected holdout MAE (pp, rounded): mean rate 2.717; linear 0.201; RF 0.256; ET 0.289; KNN 0.412. Small floating-point variation may occur across environments.

## Data dictionary
| Field | Unit | Meaning |
|---|---|---|
| time | s | Recorded timestamp |
| speed | km/h | Logged speed |
| acceleration | km/h/s | Logged acceleration |
| voltage | V | Logged terminal voltage |
| current | A | Logged signed current; positive discharge |
| power | W | Logged signed electrical power |

## Scope
Nominal 72 V and 2 kW are reported platform descriptors. The mechanical condition, pack configuration, capacity and instrument accuracy are not independently established by the log. 2.5 Ah and 25 Ah are analytical scenarios, not measured capacity. Only the supplied record is analyzed. Distance-equivalent is not verified travel distance. The reference is current-integrated, not ground truth. No learner outcomes were collected. The model uses contemporaneous features; no future samples are used in feature construction.

## Publication and citation
After author approval, create a GitHub repository, upload these files, select a license approved by the owners (data and code may need separate terms), and create a tagged release. Add the verified release URL or archived DOI to the manuscript and response. Do not claim public availability until tested from a logged-out browser. No license or permission is assumed in this candidate package.
