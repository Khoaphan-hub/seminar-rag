# Exploratory paraphrase study

One AI-authored English paraphrase per original question; answers and evidence are unchanged. This post-hoc study is retrieval-only, with no Gemini calls. The single set was frozen before scoring; no performance-based variant selection was performed. Phan Anh Khoa reviewed and accepted semantic equivalence after seeing the experiment results, without requesting query changes. No blind multi-rater review is claimed.

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m src.paraphrase_experiment
```

Inputs: `data/questions_paraphrased.json` includes original and rewritten questions, answers and evidence. Outputs: `results/paraphrase_details.json` (480 records) and `results/paraphrase_summary.json` (24 aggregates). All recomputed original aggregate metrics match the prior baseline. Model loading is offline. The full 2 methods x 2 sizes x 3 k grid is evaluated for both query sets.

At 192 tokens, k=3, evidence recall changes from .800 to .550 for TF-IDF and .625 to .550 for MiniLM. This supports a smaller decline for MiniLM at that setting, not universal superiority or improved generation. Rewordings vary syntax and length as well as lexical choices; no lexical-overlap reduction was measured.
