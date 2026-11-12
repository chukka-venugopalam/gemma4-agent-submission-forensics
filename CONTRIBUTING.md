# Contributing

Contributions that improve correctness, portability, documentation, or test coverage are welcome.

1. Keep the tools standard-library-only unless a dependency is necessary and documented.
2. Add a regression test for every bug fix.
3. Keep observed facts separate from derived statistics, inferences, and unknowns.
4. Do not describe observational score differences as causal effects.
5. Do not add private task data, credentials, access tokens, or non-redistributable competition assets.

Run the test suite from `audit_tool/` with:

```bash
python -m unittest discover -s tests -v
```
