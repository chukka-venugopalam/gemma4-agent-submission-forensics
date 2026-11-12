#!/usr/bin/env python3
"""Recompute descriptive summaries from the packaged ASFA case-study CSVs.

Uses only Python's standard library. The output is descriptive, not causal.
"""
from __future__ import annotations
import csv, itertools, json, math, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

def read_csv(name):
    with (DATA / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def mean(values):
    return statistics.mean(values) if values else None

def permutation_p(values, flags):
    """Exact two-sided permutation p for difference in group means."""
    a = [v for v, flag in zip(values, flags) if flag]
    b = [v for v, flag in zip(values, flags) if not flag]
    if not a or not b:
        return None
    observed = abs(mean(a) - mean(b))
    k, n = len(a), len(values)
    total = extreme = 0
    for idx in itertools.combinations(range(n), k):
        chosen = set(idx)
        x = [values[i] for i in idx]
        y = [values[i] for i in range(n) if i not in chosen]
        total += 1
        if abs(mean(x) - mean(y)) >= observed - 1e-12:
            extreme += 1
    return extreme / total

def analyze():
    archives = read_csv("archive_observations.csv")
    features = read_csv("factor_features.csv")
    followups = read_csv("followup_trials.csv")
    fps = {r["content_fingerprint"] for r in archives}
    baseline_fp = "abe6f1018e788f64e09cf26288f33c4d60dafd011690cf11541836dc0cc9ebaa"
    baseline = [r for r in archives if r["content_fingerprint"] == baseline_fp]
    core = [r for r in archives if (r["max_tool_calls"], r["max_time_minutes"], r["thinking_budget"]) == ("28", "8", "4096")]
    outside = [r for r in archives if r not in core]
    core_solves = [int(r["solves_if_n58"]) for r in core]
    outside_solves = [int(r["solves_if_n58"]) for r in outside]
    sd_run = statistics.stdev(core_solves)
    values = [float(r["solves_mean"]) for r in features]
    feature_cols = [k for k in features[0] if k not in {"payload_group", "archive_labels", "solves_mean", "score_records"}]
    contrasts = {}
    for key in feature_cols:
        flags = [r[key] == "1" for r in features]
        yes = [v for v, flag in zip(values, flags) if flag]
        no = [v for v, flag in zip(values, flags) if not flag]
        if not yes or not no:
            continue
        diff = mean(yes) - mean(no)
        half_width = 1.96 * sd_run * math.sqrt(1/len(yes) + 1/len(no))
        contrasts[key] = {
            "n_with": len(yes), "n_without": len(no),
            "mean_with": round(mean(yes), 2), "mean_without": round(mean(no), 2),
            "difference": round(diff, 2), "heuristic_interval": [round(diff-half_width, 2), round(diff+half_width, 2)],
            "exact_nominal_permutation_p": permutation_p(values, flags),
        }
    # Adjust the family of exploratory p-values for multiple comparisons.
    ordered_p = sorted(
        ((key, value["exact_nominal_permutation_p"]) for key, value in contrasts.items()),
        key=lambda item: item[1],
    )
    m = len(ordered_p)
    next_q = 1.0
    for rank in range(m, 0, -1):
        key, p_value = ordered_p[rank - 1]
        next_q = min(next_q, p_value * m / rank)
        contrasts[key]["bonferroni_adjusted_p"] = min(1.0, p_value * m)
        contrasts[key]["benjamini_hochberg_q"] = min(1.0, next_q)

    result = {
        "archive_records": len(archives), "distinct_payloads": len(fps),
        "baseline_same_payload_scores": [float(r["displayed_score"]) for r in baseline],
        "baseline_same_payload_solves_n58": [int(r["solves_if_n58"]) for r in baseline],
        "core_envelope": {"definition": "max_tool_calls=28, max_time_minutes=8, thinking_budget=4096", "records": len(core), "distinct_payloads": len(features), "mean_solves_n58": round(mean(core_solves), 2), "sd_solve_counts": round(sd_run, 2), "output_cap_counts": {k: sum(1 for r in core if r["max_output_tokens"] == k) for k in sorted({r["max_output_tokens"] for r in core})}},
        "outside_core_envelope": {"records": len(outside), "solve_counts_n58": outside_solves, "mean_solves_n58": round(mean(outside_solves), 2)},
        "factor_contrasts": contrasts,
        "followup_trials": [{"experiment": r["experiment"], "score": float(r["observed_score"]), "repeats": int(r["repeats"]), "interpretation": r["interpretation"]} for r in followups],
        "caveat": "58-task conversion is participant-derived; features are observational. Intervals are heuristic plug-in normal intervals, not calibrated confidence intervals. Factor contrasts use eight distinct payload means and are not randomized or causal. Follow-ups have one run per arm."
    }
    return result

if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
