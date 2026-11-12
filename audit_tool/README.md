# Agent Submission Forensics Audit (ASFA)

ASFA is a small Python-standard-library tool for auditing scored coding-agent ZIP submissions. It is designed to answer four questions before a leaderboard comparison is treated as an experiment:

1. Are two ZIPs byte-identical?
2. If not, do they contain the same files and bytes despite ZIP timestamp/compression differences?
3. What model, tools, prompt-related configuration, sampling settings, and runtime budgets are declared?
4. How many solve counts are compatible with a displayed, truncated score under an explicitly stated task-count assumption?

It writes `inventory.csv`, `duplicate_groups.csv`, and `summary.json`. An optional SafeTensors inspector checks whether LoRA B matrices are identically zero. The tools do **not** run a model, inspect hidden tasks, reproduce the evaluator, or establish causality from observational scores.

## Run

Both the archive auditor and the SafeTensors adapter inspector use the Python 3.10+ standard library only; no third-party dependencies are required.

```bash
python -m unittest discover -s tests -v
python afsa.py data/example_manifest.csv --archive-root ./archives --out ./audit_out --tasks 58
```

`data/archive_observations.csv` is an aggregate, anonymized-by-filename research manifest for the case study. It records the 14 original scored archives and their configuration metadata/fingerprints; the underlying submission ZIPs are not redistributed in this resource. To reproduce raw archive inspection, supply the corresponding archives and a two-column CSV containing `archive,score`.

## Fingerprint definition

For every regular ZIP member, ASFA records the normalized member path, byte length, and SHA-256 of the uncompressed member bytes. The sorted JSON serialization of that manifest is SHA-256 hashed to produce `content_fingerprint`. ZIP timestamps, central-directory order, and compression choices are excluded. Member paths and member contents are included. Duplicate member paths are rejected.

## Score conversion

`solve_bounds()` enumerates integer solve counts compatible with a displayed score when the display rule is floor truncation to a configurable number of decimals. The default task count of 58 is an assumption used for this case study, derived from a participant discussion and not stated as the official denominator in the Kaggle overview. Change `--tasks` and verify the display rule before applying this to another benchmark.

## Evidence and limitations

The included table is a research manifest, not raw execution data. Scores are public aggregate observations supplied by the participant. Configuration contrasts are observational. No causal effect can be inferred from this table alone. The companion paper distinguishes observed, derived, external, inferred, and unknown claims.

## License

Apache-2.0.
