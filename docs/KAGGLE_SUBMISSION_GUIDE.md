# Kaggle Paper Track submission guide

## Paper

**Title:** The ZIP Is the Treatment  
**Subtitle:** An artifact-first audit of repeated coding-agent submissions, configuration claims, and evidence quality in the Gemma 4 Developer Agent Competition  
**Author:** Chukka Venugopalam  
**Length:** approximately 2,817 words including references and figure captions (the Kaggle editor's counter is authoritative).

## Exact submission sequence

1. Open the **Google - The Gemma 4 Developer Agent Paper Track** page, not the main agent competition.
2. Create a new Writeup.
3. Paste the complete text from `Gemma4_PaperTrack_Submission.md` into the Writeup editor.
4. Upload the five PNG files from `figures/` and insert them at the matching `Figure 1` through `Figure 5` positions. The local Markdown image paths do not automatically upload the images to Kaggle.
5. Check the editor's word count. The paper is below the 3,000-word maximum, but the editor's count is the final authority.
6. Add `Gemma4_PaperTrack_Submission.pdf` as the optional public PDF/project-link artifact if the editor offers that field.
7. Upload `ASFA_Reproducible_Audit.ipynb` as a Kaggle Notebook, run it, save it, and make it public. Add that notebook in **Project Links** if you are submitting the code resource.
8. Optionally publish `ASFA_Artifact_Forensics_Resource.zip` as a public Kaggle Dataset/resource and link it from the notebook or project links. The notebook itself is self-contained; the ZIP adds the CLI, adapter inspector, raw case-study CSVs, synthetic demo archive, and tests.
9. Review the final rendered Writeup, verify each figure is visible, and press **Submit**. A saved draft is not a submission. Confirm that Kaggle shows a submitted status.

## Files to upload

- Paper body: `Gemma4_PaperTrack_Submission.md`
- Optional PDF: `Gemma4_PaperTrack_Submission.pdf`
- Editable copy: `Gemma4_PaperTrack_Submission.docx`
- Five figures: `figures/fig1_audit_pipeline.png` through `figures/fig5_lora_null_update.png`
- Reproducible notebook: `ASFA_Reproducible_Audit.ipynb`
- Companion code/data/tests: `ASFA_Artifact_Forensics_Resource.zip`

## Claim discipline

This is a single-participant forensic case study, not a claim of a better coding agent. It does not report causal configuration effects, a stable expected solve rate, hidden task outcomes, or private leaderboard rank. The 58-task conversion is a participant-derived interpretation, not an official denominator disclosure. The two follow-up arms have one run each. The notebook and resource reproduce deterministic artifact analyses, not hosted Gemma inference.

## Deadline

The official Paper Track page currently lists **November 12, 2026 at 11:59 PM UTC**, which is **November 13, 2026 at 5:29 AM India Standard Time**. The organizer can update the timeline; verify the live Kaggle page before final submission.
