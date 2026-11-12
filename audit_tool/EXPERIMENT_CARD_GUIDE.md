# Preregistered experiment card

Use `EXPERIMENT_CARD_TEMPLATE.json` before launching a model submission. It forces the investigator to record the baseline and treatment artifact hashes, exactly one changed factor, held-constant components, evaluation context, intended repetition count, primary metric, and promotion rule.

The template is not a Kaggle API integration and does not run evaluations. It is a lightweight protocol artifact intended to reduce post-hoc explanation and confounded comparisons. Replace all `REPLACE_...` placeholders before treating a card as complete.
