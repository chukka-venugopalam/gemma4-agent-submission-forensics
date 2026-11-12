# Provenance and evidence grades

| Artifact | Origin | Evidence grade | Notes |
|---|---|---|---|
| 14 archive records | Participant-provided scored ZIPs and public Kaggle scores | Observed / derived | Raw ZIPs intentionally excluded |
| Content fingerprints | SHA-256 over canonical extracted member manifests | Derived deterministically | Container metadata excluded |
| Config fields | Parsed from submitted ZIP contents | Observed | Missing keys are blank, not imputed |
| Score-to-solves field | 58-task interpretation | Assumption / derived | Not official; displayed score remains source field |
| Factor feature table | Eight distinct payloads | Derived | Non-randomized and confounded |
| I02 and B2 | Submitted one-factor ZIPs and public scores | Observed | One run per arm |
| Adapter tensor case study | Safetensors headers and tensor values | Observed | Limited to inspected participant package |
| CLI fixtures | Locally generated synthetic ZIPs | Synthetic | Tool tests only; not competition evaluations |

This dataset is not a public release of raw Kaggle competition data. It is a transformed, participant-owned archive audit record.
