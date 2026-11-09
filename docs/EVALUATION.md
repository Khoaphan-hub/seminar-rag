# Evaluation Protocol

## Retrieval

**Recall at top-k (Recall@k)** is ordinary recall evaluated using only the first k ranked results. The denominator is all relevant chunks, not k. For four relevant chunks with two found in top-3, Recall@3 = 2/4 = 0.5, whereas Precision@3 = 2/3. See [the worked explanation](RECALL_AT_K.md) and [TorchMetrics Retrieval Recall](https://lightning.ai/docs/torchmetrics/stable/retrieval/recall.html).

Q01–Q20 are answerable from the source paper. Questions, reference answers, and selected gold evidence were written before ranking. Neither questions nor answers are indexed. Both retrievers use the same 2-method × 2-size × 3-k evaluation grid.

Gold evidence consists of character spans in normalized page text, verified through exact matching. A chunk is relevant under this definition if it contains at least one complete gold span. Recall@k is the number of relevant chunks in top-k divided by all relevant chunks. The reported macro score averages over 20 questions. Chunk size changes the number of relevant chunks, so evidence-level metrics are also reported:

- **Hit@k:** whether at least one complete reference span is covered.
- **Evidence recall@k:** fraction of reference spans fully covered by the union of top-k chunks.
- **All-evidence@k:** whether every required reference span is covered; its aggregate is the fraction of questions meeting that criterion.

Gold spans are selected references, not exhaustive labels of equivalent passages. PyPI/CRAN information appears on both pages 1 and 2, for example. Missing the selected span does not always mean the answer is absent. Generation review therefore reads the actual context and source, rather than deriving correctness from Recall. Overlap may create several chunks containing one fact, reducing chunk recall even when sufficient evidence was found. Gold labels are retained for reproducibility rather than adjusted to favor a method.

## Generation

The three conditions are closed-book, TF-IDF context, and embedding context. They use the same 20 questions, model, and temperature. All receive the paper title, Jin Zhu et al., year 2022, and JMLR 23, pages 1–7, so the baseline is not penalized for an ambiguous paper identity. Both RAG conditions use chunk size 192 and k=3; their prompts differ only in retrieved passages. Closed-book instructions allow existing knowledge, request uncertainty when appropriate, and prohibit pretending to have checked sources. Calls are independent, with condition order rotated across questions.

`generation_pilot.jsonl` predates the matched-metadata prompts and is excluded from the main results.

Evaluate three distinct aspects:

1. **Correctness:** 1 for all core reference facts correctly answered; 0.5 for a partial answer, overbroad qualification, or imperfect explanation retaining the central point; 0 for an incorrect target fact, no answer, or abstention. This rubric involves judgment. See per-response rationales in `answer_review.csv`. A cautious abstention is not a correct answer to an answerable question.
2. **Groundedness (RAG):** whether factual claims are supported by the actual supplied context. Even a true statement exceeds the supplied evidence if absent from that context. Complete abstentions are marked separately and are not counted as fully correct factual answers.
3. **Citation support (RAG):** whether the cited ID occurs in the prompt and its passage supports the attached claim. Matching an ID with a regular expression does not establish semantic support or detect every malformed reference.

Reviewers must read both response and context and record a rationale. AI-assisted review must not be called independent human evaluation. Lexical similarity to a reference is not sufficient to establish correctness.

The English rationale field is `rationale_en`. The translation preserves scores, answer hashes, and the original Gemini records. `src/review_generation.py` exports fixed assisted annotations; running it does not perform a new blind evaluation.

## Failure Categories

- **Missing retrieval:** top-k lacks the required information.
- **Incorrect retrieval:** returned passages match the topic or words but do not answer the question.
- **Irrelevant citation:** the cited passage does not support the attached claim.
- **Beyond evidence:** the answer adds information absent from its context, even if found elsewhere in the full PDF.

A response can have multiple failure types. Constructed examples must be labeled hypothetical and excluded from counts of observed model failures.

## Review acceptance

Phan Anh Khoa (24125059) and Bùi Trọng Thành (24125043) each confirmed that they reviewed and agreed with the assisted evaluation. Scores and rationales remain unchanged. This acceptance does not establish blind re-scoring or inter-rater agreement. See `REVIEW_SIGNOFF.md`.
