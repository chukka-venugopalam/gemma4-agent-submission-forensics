#!/usr/bin/env python3
"""Artifact-First Submission Audit (AFSA), Python standard library only."""
from __future__ import annotations
import argparse, csv, hashlib, json, re, zipfile
from collections import defaultdict
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_payload(zip_path: Path):
    """Return a timestamp-independent fingerprint and deterministic member manifest."""
    members = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        seen = set()
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename.replace("\\", "/")
            if name in seen:
                raise ValueError(f"duplicate ZIP member path: {name}")
            seen.add(name)
            data = zf.read(info)
            members.append({"path": name, "size": len(data), "sha256": sha256_bytes(data)})
    members.sort(key=lambda x: x["path"])
    canonical = json.dumps(members, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(canonical), members


def _read_member(zip_path: Path, target: str) -> str:
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            return zf.read(target).decode("utf-8", errors="replace")
    except KeyError:
        return ""


def _scalar(text: str, key: str):
    m = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*([^\n#]+)", text)
    if not m:
        return ""
    return m.group(1).strip().strip('"\'')


def inspect_config(zip_path: Path):
    agent = _read_member(zip_path, "agent.yaml")
    sampling = _read_member(zip_path, "configs/sampling.yaml")
    evaluation = _read_member(zip_path, "eval_config.yaml")
    tools = []
    in_tools = False
    for line in agent.splitlines():
        if re.match(r"^tools\s*:", line):
            in_tools = True
            continue
        if in_tools and line and not line[0].isspace():
            break
        if in_tools:
            m = re.match(r"^\s+-\s*([A-Za-z_][A-Za-z0-9_]*)", line)
            if m:
                tools.append(m.group(1))
    adapters = sorted({p.split("/")[1] for p in _member_names(zip_path) if p.startswith("adapters/") and len(p.split("/")) > 2})
    return {
        "model": _scalar(agent, "model"),
        "root_tool_count": len(tools),
        "root_tools": ";".join(tools),
        "temperature": _scalar(sampling, "temperature"),
        "top_p": _scalar(sampling, "top_p"),
        "top_k": _scalar(sampling, "top_k"),
        "max_output_tokens": _scalar(sampling, "max_output_tokens"),
        "thinking_budget": _scalar(sampling, "thinking_budget"),
        "include_thoughts": _scalar(sampling, "include_thoughts"),
        "max_tool_calls": _scalar(evaluation, "max_tool_calls"),
        "max_time_minutes": _scalar(evaluation, "max_time_minutes"),
        "max_turns": _scalar(evaluation, "max_turns"),
        "timeout_seconds": _scalar(evaluation, "timeout_seconds"),
        "adapter_dirs": ";".join(adapters),
    }


def _member_names(zip_path: Path):
    with zipfile.ZipFile(zip_path, "r") as zf:
        return [i.filename for i in zf.infolist() if not i.is_dir()]


def solve_bounds(displayed_score: float, task_count: int = 58, decimals: int = 2):
    """Solve counts consistent with floor-truncated displayed score."""
    target = int(round(displayed_score * (10 ** decimals)))
    factor = 10 ** decimals
    matches = [k for k in range(task_count + 1) if (factor * k) // task_count == target]
    if not matches:
        return "", ""
    return min(matches), max(matches)


def audit_manifest(manifest: Path, archive_root: Path, out: Path, task_count: int = 58):
    out.mkdir(parents=True, exist_ok=True)
    inventory, groups = [], defaultdict(list)
    with manifest.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = row["archive"]
            score = float(row["score"])
            zp = archive_root / name
            if not zp.is_file():
                raise FileNotFoundError(zp)
            archive_hash = sha256_bytes(zp.read_bytes())
            fingerprint, members = canonical_payload(zp)
            low, high = solve_bounds(score, task_count)
            config = inspect_config(zp)
            item = {
                "archive": name, "score": f"{score:.2f}",
                "solves_min": low, "solves_max": high,
                "archive_sha256": archive_hash,
                "content_fingerprint": fingerprint,
                "member_count": len(members),
                **config,
            }
            inventory.append(item)
            groups[fingerprint].append(name)
    fields = list(inventory[0]) if inventory else []
    with (out / "inventory.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(inventory)
    dupes = [{"content_fingerprint": k, "count": len(v), "archives": ";".join(v)} for k,v in groups.items() if len(v)>1]
    with (out / "duplicate_groups.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["content_fingerprint","count","archives"]); w.writeheader(); w.writerows(dupes)
    summary = {
        "records": len(inventory), "distinct_payloads": len(groups),
        "duplicate_groups": len(dupes), "task_count_assumption": task_count,
        "score_mapping_note": "Solve counts are compatible with floor-truncated displayed scores; verify denominator and display rule for the target competition.",
        "causal_note": "This utility fingerprints and inventories artifacts. It does not establish causal effects from observational submission scores.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path, help="CSV with columns archive,score")
    ap.add_argument("--archive-root", type=Path, default=Path("archives"))
    ap.add_argument("--out", type=Path, default=Path("audit_out"))
    ap.add_argument("--tasks", type=int, default=58)
    args = ap.parse_args()
    print(json.dumps(audit_manifest(args.manifest, args.archive_root, args.out, args.tasks), indent=2))

if __name__ == "__main__":
    main()
