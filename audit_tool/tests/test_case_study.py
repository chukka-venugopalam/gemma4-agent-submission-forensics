import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analyze_case_study as case

class CaseStudyTests(unittest.TestCase):
    def test_archive_and_payload_counts(self):
        r = case.analyze()
        self.assertEqual(r["archive_records"], 14)
        self.assertEqual(r["distinct_payloads"], 12)

    def test_repeated_baseline_outcomes(self):
        r = case.analyze()
        self.assertEqual(r["baseline_same_payload_scores"], [0.15, 0.17, 0.2])
        self.assertEqual(r["baseline_same_payload_solves_n58"], [9, 10, 12])

    def test_core_envelope_output_cap_split_is_disclosed(self):
        r = case.analyze()["core_envelope"]
        self.assertEqual(r["records"], 10)
        self.assertEqual(r["output_cap_counts"], {"16384": 1, "8192": 9})

    def test_exploratory_bundled_contrast(self):
        r = case.analyze()["factor_contrasts"]["max_turns_100_timeout_300"]
        self.assertEqual(r["difference"], 3.11)
        self.assertEqual(r["exact_nominal_permutation_p"], 0.036)

    def test_followup_scores(self):
        r = case.analyze()
        self.assertEqual([x["score"] for x in r["followup_trials"]], [0.12, 0.15])

if __name__ == "__main__": unittest.main()
