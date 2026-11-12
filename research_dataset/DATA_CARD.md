# ASFA Public Research Dataset v1.1 — Data Card

## Summary
A compact, participant-specific dataset of 14 scored Gemma 4 Developer Agent submission archives, their extracted-payload fingerprints, declared configuration features, and two later one-factor follow-up submissions. It supports reproducibility and archive-level experimental auditing; it is not a benchmark of model-generated patches.

## Intended uses
- Demonstrate byte-level and payload-level deduplication concepts.
- Inspect how declared configuration metadata maps to submission records.
- Recompute descriptive score summaries and exploratory factor contrasts.
- Preregister future agent experiments with an artifact-hash and decision-rule template.
- Teach preregistration and provenance practices for agent experiments.

## Out-of-scope uses
- Predicting private leaderboard rank or hidden-test outcomes.
- Claiming causal effects from observational configuration contrasts.
- Training a coding agent or evaluating generated patches.
- Treating solve counts derived from the 58-task assumption as official task-level labels.

## Unit of observation
`historical_submissions.csv`: one scored ZIP record. `payload_groups.csv`: one unique extracted payload fingerprint. `factor_features.csv`: one of eight distinct payload-level feature rows used for the exploratory contrasts. `followup_trials.csv`: one one-factor follow-up run per arm.

## Collection and provenance
The 14 historical rows were derived from participant-provided submission ZIPs and public Kaggle score observations. Raw submission archives are not redistributed. Follow-up rows I02 and B2 were matched to their experiment ZIPs by SHA-256. Configuration fields were parsed from the archived submission contents. The adapter case study is based on direct SafeTensors header/tensor inspection of one participant-provided archive.

## Transformations and assumptions
- `archive_sha256` hashes the full ZIP container.
- `content_fingerprint` hashes sorted member paths, member lengths, and SHA-256 hashes of uncompressed member bytes; ZIP timestamps/compression metadata do not affect it.
- `solves_if_n58` is a participant-derived interpretation assuming 58 tasks and floor-truncated two-decimal scores. The competition overview does not establish 58 as the official denominator. Use `displayed_score` as the observed field; treat solve counts as an assumption.
- Factor contrasts use eight distinct payload-level means. They are observational, confounded, and exploratory.
- Exact permutation p-values are unadjusted nominal tests; adjusted Bonferroni and Benjamini-Hochberg columns are provided for the family of 16 exploratory contrasts. None survives adjustment at 0.05.
- Heuristic intervals are not calibrated small-sample confidence intervals.

## Limitations and known gaps
No per-task result vector, model trace, tool-call log, generated patch, evaluator version receipt, or private leaderboard outcome is included. The two follow-up arms each have one run. This dataset cannot estimate expected score or establish causality.

## Privacy and licenses
The dataset contains only aggregate competition observations and fingerprints of the participant's own submitted archives; raw ZIPs and account screenshots are excluded. Dataset tables are released under CC BY 4.0. The ASFA source code is Apache-2.0.
