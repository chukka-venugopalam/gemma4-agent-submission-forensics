# Evidence ledger for the accompanying paper

| Claim | Evidence class | Basis | Limitation |
|---|---|---|---|
| 14 archives contain 12 distinct extracted payloads | Observed / derived | Member-level hashes from user-provided archives | Applies to this archive set only |
| Baseline payload scored 0.15, 0.17, 0.20 | Observed | Public Kaggle results and identical payload hashes | Three runs; source of variation unknown |
| 58-task conversion | External / derived | Participant discussion score lattice | Not an official denominator statement |
| 10 in-regime archive records average 9 solves | Derived | Historical score table converted using 58-task assumption | Includes three repeated copies of one payload |
| Four out-of-regime records average 2.5 solves | Derived | Same table | Multiple confounded settings |
| 15 of 16 in-regime factor intervals include zero; one bundled turn/timeout interval is marginally positive | Derived | Small-sample exploratory analysis in M24R | 8 distinct payloads; not randomized |
| I02 scored 0.12; B2 scored 0.15 | Observed | Submitted ZIP SHA-256 matches scored archives | One run per arm |
| Two adapter B matrices are zero | Observed | SafeTensors tensor inspection | Specific adapter package only |
| M3 source snapshots were 0/129 | Observed in package provenance | M3 README and missing snapshot manifest | Says nothing about other participants' assets |
| M4 19 tests passed | Observed local | M4 test log | Synthetic fixtures, not live agent evaluation |

Do not convert an inference, external result, or synthetic test into a claim about this agent's measured performance.
