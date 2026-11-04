# CS420 S07 — Retrieval-Augmented Generation

An English seminar report on document retrieval and evidence verification. The experiment uses **abess: A Fast Best-Subset Selection Library in Python and R**, Zhu et al. (2022), seven pages under **CC BY 4.0**.

| Team member | Student ID |
|---|---|
| Phan Anh Khoa | 24125059 |
| Bùi Trọng Thành | 24125043 |

## Deliverables

**Compiled report:** [PDF](report/main.pdf). **Editable source:** [LaTeX](report/main.tex).

**Existing Canva slides:** https://canva.link/abw5shp7wrkofnm

The report and supporting documents are in English. The Canva deck and the entire `slides/` directory remain unchanged at the team's request; their translation is deferred.

- `report/`: report source, PDF, and experiment tables.
- `data/questions.json`: 20 English questions, reference answers, source pages, and evidence spans.
- `data/sources/`: licensed source PDF and provenance manifest.
- `src/`: extraction, TF-IDF/embedding retrieval, Gemini generation, and review exports.
- `results/`: measured results and per-question logs, distinct from published paper results.
- `docs/`: evaluation rubric, AI disclosure, team presentation plan, Q&A, and submission checklist.

## One shared RAG pipeline, two retrievers

```text
src/
  prepare.py           PDF extraction and normalization
  retrievers/
    tfidf.py           Lexical TF-IDF + cosine similarity
    embedding.py       Dense MiniLM + cosine similarity
    __init__.py        Retriever selection and shared stable top-k ranking
  demo.py              Inspect either retriever and its context/prompt
  experiment.py        Shared chunks, both retrievers, retrieval evaluation
  generate.py          Gemini: closed-book / TF-IDF RAG / embedding RAG
  review_generation.py Answer review export
  build_tables.py      Report table export
tests/                 Evidence checks and retrieval regression checks
```

The main data flow is PDF → pages → identical chunks → TF-IDF **or** MiniLM
→ top-k context → shared prompt → Gemini. The controlled generator reads the
saved retrieval records so every generated answer is bound to a recorded context.
Closed-book generation omits retrieved context. The demo displays retrieval and
optionally the prompt; it does not call Gemini.

Use the root `.venv` for current work. In VS Code, select
`.venv/Scripts/python.exe` with **Python: Select Interpreter** if another
interpreter was previously selected. This repository is self-contained; the
original prototype is stored outside the Seminar directory and is not required.

## Reproduce the experiment

Use Python 3.11 or later and a dedicated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.prepare
.\.venv\Scripts\python.exe -m src.experiment
```

The first embedding run downloads `sentence-transformers/all-MiniLM-L6-v2`. Add `--offline` to the last command if the model is already cached. `requirements-lock.txt` records the historical environment used for the original experiment, including extra prototype dependencies; `requirements.txt` lists the seminar pipeline's direct dependencies.

Both retrievers use identical chunks of 96/192 **WordPiece tokens**, 24-token overlap, cosine similarity, and k=1/3/5. Search is exhaustive. Higher cosine means greater similarity, not a calibrated probability of answer correctness.

Inspect a question without an API call:

```powershell
.\.venv\Scripts\python.exe -m src.demo --method tfidf --question "What test coverage is reported for Python and R?" --prompt
.\.venv\Scripts\python.exe -m src.demo --method embedding --question "What test coverage is reported for Python and R?" --prompt
```

## Gemini generation

Create a local `.env` in the Seminar root based on `.env.example` and set your own API key. The generator reads only this local configuration file (or existing environment variables). Credentials are excluded from results and Git.

```powershell
.\.venv\Scripts\python.exe -m src.generate --limit 60 --delay 10
```

Each question has three independent conditions: closed-book, TF-IDF RAG, and embedding RAG. All receive the same paper-identifying metadata. Both RAG conditions use 192-token chunks and k=3, selected before inspecting results. Temperature is 0, with at most 2048 output tokens. Successful records are saved to JSONL and skipped on resumption when question, condition, model, and prompt hash match. The program stops on API/quota errors. `--limit` caps new calls rather than questions. It does not automatically switch to a paid plan.

The final experiment uses `gemini-3.5-flash-lite`. Earlier 3.8 requests timed out, and 2.5 Flash-Lite requests were rejected for the account. These failures are not scored as wrong answers. Do not change models within a comparison.

## Evaluation and checks

**Recall@k means recall among the first k ranked results.** See [the definition and worked example](docs/RECALL_AT_K.md). The assignment's notation is valid; the experiment retains it and makes the cutoff explicit.

There are 240 retrieval records (20 questions × 2 methods × 2 sizes × 3 k values) and 60 final Gemini responses. Assisted review found 5/20 fully correct closed-book answers, 16/20 with TF-IDF, and 14/20 with MiniLM. Both team members must independently review `results/answer_review.csv`. The English rationale column is `rationale_en`; scores and original responses are preserved.

`generation_pilot.jsonl` is excluded from the final results because its baseline prompt lacked matching paper-identifying metadata.

```powershell
.\.venv\Scripts\python.exe -m src.review_generation
.\.venv\Scripts\python.exe -m src.build_tables
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The review exporter contains fixed, editable assisted annotations. Rerunning it exports those annotations; it does not perform a new independent evaluation and will overwrite manual edits to the CSV. Make any agreed label changes in the exporter as well.

## Compile the report

```powershell
cd report
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

XeLaTeX uses Times New Roman and Consolas. On a system without these fonts, choose installed alternatives supporting the authors' Vietnamese names, such as TeX Gyre Termes and Latin Modern Mono. Measured retrieval and generation tables are in `retrieval_table.tex` and `generation_results.tex`.

## Collaboration

Private repository: https://github.com/Khoaphan-hub/seminar-rag

The owner can invite a collaborator through **Settings → Collaborators → Add people**. Work on separate branches and use pull requests. Only one person should regenerate shared results at a time. Canva access is managed separately through **Share**.

Do not commit API keys, Python environments, model weights, or vector-store caches. The instructor's assignment PDF and foundational papers remain local; citations are provided without assigning them a new license.

## Limitations

This is a descriptive study with 20 deliberately authored questions, one paper, one small embedding model, and one generation per condition. Selected gold spans do not exhaust equivalent evidence. Retrieval recall is not LLM accuracy, and these results do not establish a general lexical-versus-dense ranking. Public-paper training contamination cannot be ruled out.

See `THIRD_PARTY_NOTICES.md`, `docs/EVALUATION.md`, and `docs/AI_DISCLOSURE.md`.
