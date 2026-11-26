# Student worksheet — Engineering SOC estimation
Proposed undergraduate laboratory | Two 90-minute sessions | Individual submission (collaboration for troubleshooting allowed)

**Prerequisites:** electrical quantities, signed numerical integration, introductory regression, Python or spreadsheet. **Materials:** `data/ev_log.csv`, Python/Jupyter or spreadsheet, calculator. Do not operate an EV or battery for this data-only exercise.

## Session 1 — Measurement and reference (90 minutes)
1. **15 min: prediction.** Before running code, predict whether 2 kW is the measured load and whether terminal voltage can determine capacity. Record your reasoning.
2. **20 min: signal audit.** Check count, units, timestamps, duplicates, missing values, sign and ranges. Identify measured/logged versus calculated quantities. Calculate the speed-integral distance-equivalent; explain what it cannot establish. Submit an annotated signal table.
3. **30 min: SOC computation.** Use dt[0]=0, dt[k]=1 s for later records; ΔSOC[k] = −100 I[k] dt[k]/(3600 C). Compute signed net Ah and Wh. Show one nonzero update manually using an actual row. Plot the trajectories at 2.5 and 25 Ah, with initial SOC 100% and efficiency 1. Submit executable calculations.
4. **25 min: uncertainty.** Compare voltage variation with both scenarios. Explain why capacity, initial SOC, chemistry and sensor calibration matter. Write a qualified conclusion; propose an independent check.

## Session 2 — Chronological model evaluation (90 minutes)
1. **15 min: prediction.** Sketch the expected absolute-SOC result if future SOC is below the training range. Explain why a random split might conceal this issue without claiming a measured random-split result.
2. **25 min: direct regression.** Use rows 1–5,858 for training and 5,859–7,323 for holdout. Fit RF, ET and KNN on absolute SOC. Use speed, acceleration and voltage, one-sample lag and causal five-sample means. Exclude current and power. Standardize KNN using training data only.
3. **25 min: delta regression.** Predict signed increments using the same features; reconstruct from the last training SOC. Add a constant training-mean increment baseline and ordinary least-squares regression. Calculate MAE, RMSE, R² and signed endpoint error. Explain what the model can and cannot infer.
4. **15 min: compare.** Inspect cumulative signed errors and the three expanding-window fold results (train lengths 2929, 3905, 4881; subsequent validation lengths 976, 976, 977). Compare simple and complex models. Explain why folds are not independent vehicle trials.
5. **10 min: individual exit response.** State one supported finding, two limitations, and a proposed next experiment. Disclose AI assistance and describe how any generated calculation was checked.

## Submit
Signal audit, executable calculation and capacity plot, model metric table and reconstruction/error plots, interpretation and limitation statement. Include units and identify all assumed quantities. Do not call the current-integrated reference actual SOC. The rubric is formative (0–15 points); it has not been validated.
