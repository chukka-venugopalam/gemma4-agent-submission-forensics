# Publish this repository on GitHub

Recommended repository name: `gemma4-agent-submission-forensics`

Suggested description: `Reproducible artifact-first audit of Gemma 4 coding-agent submissions: ZIP fingerprinting, configuration extraction, score-variation analysis, and LoRA tensor inspection.`

Suggested topics: `gemma`, `coding-agents`, `software-engineering`, `reproducibility`, `benchmarking`, `artifact-forensics`, `safetensors`, `kaggle`, `python`.

## Using the ZIP

1. Download and extract `Gemma4_Agent_Submission_Forensics_GitHub_Repo.zip`.
2. Create a **public** repository on GitHub named `gemma4-agent-submission-forensics`. Do not initialize it with another README, license, or `.gitignore`; those files are already included.
3. Open a terminal in the extracted `gemma4-agent-submission-forensics` folder and run:

```bash
git init
git add .
git commit -m "Add Gemma 4 agent submission forensics paper and artifacts"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/gemma4-agent-submission-forensics.git
git push -u origin main
```

4. Replace `YOUR-USERNAME` with your GitHub username.
5. Open the public repository page and copy its URL.
6. In the Kaggle Paper Track Writeup, under **Attachments → Project links**, add that public GitHub URL with the label `Code and reproducibility artifacts (GitHub)`.

Do not claim the paper has a public repository until the push succeeds and the repository page is accessible without signing in.
