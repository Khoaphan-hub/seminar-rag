# S07 Requirement Checklist

Team: **Phan Anh Khoa — 24125059** and **Bùi Trọng Thành — 24125043**.

| Requirement | Location or status |
|---|---|
| Parametric/non-parametric memory; RAG vs fine-tuning/full prompt | Report: Background |
| Pipeline and stage-specific failures | Background and pipeline failure analysis |
| Licensed corpus of 5–10 pages | `data/sources/abess_2022.pdf`, 7 pages, CC BY 4.0 |
| 15–20 questions with references and sources | `data/questions.json`, 20 questions |
| Retrieval with at least two chunk sizes or k values | `src/experiment.py`: 2 methods × 2 sizes × 3 k values |
| Recall@k table | `results/retrieval_summary.csv`, `report/retrieval_table.tex` |
| Same questions with/without retrieval | `results/generation.jsonl`, 60 final responses |
| Symbols, ranges, assumptions, numerical example | Report: Method and Worked Example |
| Question, chunks, answer, and citation example | Q08 in the report |
| At least three analyzed failures | Q06, Q13, Q09, plus Q14/Q15 generation analysis |
| Verification and source updates | Report: Results and Discussion (verification, updates, limitations) |
| Required paper and Sequence/Token comparison | Report: Background and Method |
| A4 report, 6–10 content pages | English LaTeX/PDF edition requested by the team; the instructor permits 1–2 additional content pages, as reported by the team |
| Team names and student IDs | Report title block and README |
| Presentation: 8–12 slides, 15 minutes | Pending: local slide files removed; content planning deferred |
| Five-minute Q&A, participation by every member | Two-person plan in `docs/PRESENTATION_AND_QA.md` |
| Attribution for data, tables, diagrams, equations, and AI | Bibliography, captions, notices, AI disclosure |

## Before Submission

- Evaluation acceptance recorded: Phan Anh Khoa and Bùi Trọng Thành reviewed and agreed with the assisted results; see `REVIEW_SIGNOFF.md`.
- Rehearse the 15-minute talk and ensure both members answer at least one question during Q&A.
- Review the instructor's language and submission instructions against the team's requested English edition.
- Confirm the deadline, submission channel, and filename requirements in the instructor's separate announcement; the assignment PDF gives no specific date.
- Invite the intended collaborator separately to GitHub and Canva. Do not share API keys.
- Prepare a new slide deck after agreeing on its content. The local `slides/` folder is empty; the external Canva design was not deleted.
