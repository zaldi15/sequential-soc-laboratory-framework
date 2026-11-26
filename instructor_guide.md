# Instructor guide and formative rubric
This is a proposed, unpiloted instructional package, not empirical evidence of educational effectiveness.

## Preparation and facilitation
Run the solution notebook before class; distribute the dataset and worksheet, not the solution until students have made initial predictions. Confirm that students understand units, sign, a causal window and the train/test boundary. For courses without EV access use the provided log; for spreadsheet-only delivery emphasize Session 1 and use supplied prediction outputs for interpretation. Pair students for troubleshooting; assess individual reasoning. No battery handling is required. Allow AI only with disclosure and independent verification of code, units and interpretation.

## Solution checkpoints
- 7,323 samples; 1 s interval; 7,322 s elapsed; no missing records. Maximum electrical power 128.52 W; motor rating 2 kW is not measured load. Speed integral 48.99 km is a distance-equivalent, not verified travel.
- Net 1.1069 Ah and 78.840 Wh; final pseudo-reference 55.73% (2.5 Ah) and 95.57% (25 Ah). Voltage 70.8–71.5 V; this does not establish physical capacity. Illustrative 1 A for 1 s gives −0.01111 pp at 2.5 Ah; students must also show an actual row calculation.
- 5,858 training and 1,465 holdout rows. No random-split metrics are reported. Exclude current/power; no future feature values; fit KNN scaler only on training.
- Linear regression holdout MAE 0.201 pp, RMSE 0.244 pp and R² 0.996. Constant baseline MAE 2.717 pp. The lowest mean fold MAE is linear regression (0.103 pp). These are reference agreement metrics and are conditional on capacity and initialization. Use `results/` for full tables and plots.
- Direct RF, ET and KNN yield strongly negative R² because test targets are below training range. The errors in accumulated predicted increments can drift. Require independent reference SOC and additional documented runs to assess generalization.

## Analytic rubric (0–3 per criterion; total 15)
| Criterion | 0 absent | 1 emerging | 2 adequate | 3 strong |
|---|---|---|---|---|
| Signal audit | No evidence | Lists signals | Correct units and sign | Also explains provenance and no-load scope |
| SOC calculation | Missing | Formula with errors | Correct signed calculation | Also explains capacity and initial-state uncertainty |
| Validation | Missing | Split unclear | Causal 80:20 split | Also explains leakage, baseline and extrapolation |
| Uncertainty | Missing | Unqualified metric | Distinguishes pseudo-reference | Also explains drift, quantization and independent checks |
| Communication | Missing | Unsupported claim | Clear evidence and limitations | Explicit qualified claim with justified next test |

Score each artifact against the highest descriptor fully supported by evidence. Give criterion-specific feedback, not a grade based solely on R². For future research, obtain institutional approval as applicable, seek expert review of task/rubric alignment and examine inter-rater agreement before claiming validity.

## Anticipated errors and instructional responses
| Anticipated error (not observed learner data) | Instructor prompt |
|---|---|
| 2 kW treated as measured power | Compare rated and observed quantities. |
| Missing 3600 conversion or reversed current sign | Recalculate one row with units. |
| 25 Ah taken as verified from flat voltage | What independent measurement or label would establish capacity? |
| Current/power used as features | Trace the algebraic dependence of ΔSOC on current. |
| Random shuffle or centered rolling mean | Which information would be available at estimation time? |
| High R² equals true SOC accuracy | What reference was used? Which uncertainty remains? |
| Fold count equals repeated experiments | Identify where all validation records came from. |
| Negative R² means all nonlinear models are inferior | Discuss target support, baseline and scope. |
