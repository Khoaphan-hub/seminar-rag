# Understanding Recall at Top-k

Recall@k (read “recall at k”) is ordinary recall when the returned set is restricted to the first k ranked results. The suffix describes the retrieval cutoff; it is not an error in the metric name. The S07 assignment explicitly requests top-k hit rate or Recall@k and a Recall@k results table.

For a question q:

- R_q: all chunks labeled relevant under the evaluation protocol.
- T_q,k: the first k chunks returned by the retriever.
- Recall@k(q) = |R_q ∩ T_q,k| / |R_q|.

The denominator is the total number of relevant chunks, not k. Equivalently, recall is TP/(TP+FN), where retrieved relevant chunks are true positives and missed relevant chunks are false negatives.

## Worked Example

Assume four relevant chunks: A, B, C, and D. The top-3 results are A, X, and C, where X is irrelevant.

| Metric | Calculation | Result |
|---|---|---|
| Recall@3 | 2 relevant chunks retrieved / 4 relevant chunks in total | 0.5 |
| Precision@3 | 2 relevant chunks retrieved / 3 retrieved chunks | 0.667 |
| Hit@3 | At least one relevant chunk appears in top-3 | 1 |

“Recall = 0.5” is also correct if the returned set has already been specified. “Recall@3 = 0.5” makes that set's rank cutoff explicit. The suffix is useful when comparing k=1, 3, and 5. It does not mean the probability that an LLM answer is correct.

## Interpretation in This Project

A chunk is relevant if it contains a complete selected gold evidence span. The report gives the arithmetic mean of per-question chunk Recall@k across 20 questions. The stored field is `chunk_recall`, with k recorded in a separate field.

At chunk size 192 and k=3, macro Recall@3 is 0.800 for TF-IDF and 0.600 for MiniLM. This is an average fraction of relevant chunks recovered; it is not automatically the fraction of correctly answered questions.

Overlap can produce multiple relevant chunks containing one fact. Selected gold spans may also omit equivalent evidence elsewhere. Therefore the project additionally reports evidence-span recall, evidence hit, and all-evidence coverage, and reviews generated answers separately. The project's `hit` field checks whether at least one selected evidence span is covered by the union of retrieved chunks; this is an evidence-level variant, not a universal definition of document hit rate.

For a fixed ranking and relevance set, increasing k cannot reduce recall because the returned sets are nested. It can still add irrelevant context and need not improve generation. Retrieving the entire corpus yields recall 1 when relevant chunks exist, but removes the useful selection step.

## Reference

[TorchMetrics: Retrieval Recall](https://lightning.ai/docs/torchmetrics/stable/retrieval/recall.html) defines recall over relevant documents and supports Recall@K through the `top_k` cutoff. Accessed 29 October 2026. Our experiment computes the metric directly rather than using this library.
