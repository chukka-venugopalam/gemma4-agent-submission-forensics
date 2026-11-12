# ASFA Public Research Dataset v1.1

This is the machine-readable companion dataset for **The ZIP Is the Treatment** (Gemma 4 Developer Agent Paper Track).

## Contents
- `data/historical_submissions.csv` and `.jsonl`: 14 scored archive records with both ZIP and extracted-payload hashes.
- `data/payload_groups.csv`: 12 unique extracted payloads and their observed scores.
- `data/factor_features.csv`: eight payload-level rows for 16 exploratory feature contrasts.
- `data/factor_contrasts_adjusted.csv`: exact nominal permutation p-values plus Bonferroni and Benjamini-Hochberg adjustments.
- `data/followup_trials.csv`: the I02 and B2 single-run follow-ups.
- `data/adapter_case_study.json`: tensor-level zero-LoRA-update case study.
- `analysis/summary.json`: recomputed summary.
- `tools/`: standard-library archive fingerprint/config parser, case-study analysis and SafeTensors inspector.
- `tests/` and `examples/`: regression tests and a synthetic ZIP fixture.
- `notebooks/ASFA_Reproducible_Audit_v1_1.ipynb`: self-contained executable analysis.
- `figures/`: small plots generated from the packaged observations.

## Run
Requires Python 3.10+ for the CLI and tests. The audit scripts use only the Python standard library.

```bash
python -m unittest discover -s tests -v
python tools/analyze_case_study.py
python tools/afsa.py examples/demo_manifest.csv --archive-root examples/demo_archives --out demo_out --tasks 58
```

Open `notebooks/ASFA_Reproducible_Audit_v1_1.ipynb` in Kaggle or Jupyter. It embeds the aggregate tables and does not need internet access or private archives.

## Key result, carefully stated
Fourteen historical archive records reduce to 12 extracted payloads. One baseline payload appears with public scores 0.15, 0.17 and 0.20. This establishes observed score variation for this participant's payload, not its cause. The two one-factor follow-ups scored 0.12 and 0.15, one run each. No causal improvement is established.

## Reproducibility cautions
The 58-task solve-count conversion is an assumption, not an official denominator. The factor analysis is based on eight distinct payloads, is observational and exploratory, and tests 16 features. The lowest nominal p-value is approximately 0.0357, but its Bonferroni-adjusted p and BH q are both approximately 0.5714. No contrast survives multiple-testing adjustment.

## Experiment protocol

Before running another arm, copy `EXPERIMENT_CARD_TEMPLATE.json`, replace all placeholders, and register the exact artifact hashes and decision rule. This template is a protocol aid; it does not run Kaggle evaluations.

## License
Dataset tables: CC BY 4.0 (`DATA_LICENSE.txt`). Code: Apache-2.0 (`CODE_LICENSE.txt`).
