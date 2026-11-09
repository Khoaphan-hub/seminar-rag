# Team Presentation Plan and Q&A

| Presenter | Student ID | Suggested slides | Time | Focus |
|---|---|---|---|---|
| Phan Anh Khoa | 24125059 | 1–6 | 7 min 30 sec | Research question, memory, pipeline, equations, corpus, retrievers |
| Bùi Trọng Thành | 24125043 | 7–12 | 7 min 30 sec | Metrics, retrieval/generation results, examples, failures, verification |

This is a proposed allocation for two members, not a claim of completed work or rehearsal. Suggested slide durations are 60, 75, 75, 90, 60, 90 seconds for slides 1–6, and 75, 75, 75, 90, 75, 60 seconds for slides 7–12. Total: 900 seconds.

Both members should answer at least one question during the five-minute Q&A. Rehearse the demo and keep saved response logs available if the free API or classroom network is unavailable.

The local `slides/` folder is empty. The allocation above is provisional; slide content will be discussed later. The Q&A below remains useful for studying the report.

## Discussion Questions and Suggested Answers

1. **Does RAG eliminate hallucination?** No guarantee follows from retrieval alone. Failures can originate in the source, extraction, retrieval, prompting, generation, or citation. This small experiment illustrates mechanisms rather than measuring all possible hallucinations.
2. **Why does TF-IDF outperform MiniLM here?** Many questions contain exact API names and paper-specific terms. MiniLM is small and not adapted to this corpus. This is a plausible interpretation, not a causal conclusion. Independent paraphrases and additional models would help test it.
3. **Does TF-IDF also use cosine?** Yes. Both sparse TF-IDF vectors and dense embeddings can be compared using cosine; their representations differ.
4. **Why count tokens when chunking?** MiniLM accepts at most 256 tokens. Both selected sizes, including special tokens, fit without truncation. These are MiniLM WordPiece tokens, not characters or Gemini billing tokens.
5. **Is Recall@k answer accuracy?** No. Recall evaluates retrieval against relevant evidence labels. Correctness evaluates answer content; groundedness evaluates support from actual context.
6. **Does increasing k always help?** Recall cannot decrease for nested top-k sets, but more context can add noise and cost. Generation is evaluated only at k=3 here, so its response to changing k was not measured.
7. **How does RAG-Sequence differ from concatenating three chunks?** The paper marginalizes the probability of an entire output sequence over latent documents. The demo concatenates context and calls an API; it does not reproduce that marginalization.
8. **Does RAG-Token search again for every token?** Its latent document can vary across token positions within the retrieved set. The equation does not require running a new search each time.
9. **Can RAG be fine-tuned?** Yes. Lewis et al. train the query encoder and generator while keeping the document encoder and index fixed. This demo uses pretrained components.
10. **Does non-parametric mean the retriever has no parameters?** No. The external knowledge store is non-parametric memory, but its query and document encoders can have learned parameters.
11. **Why are the article and software licenses different?** CC BY 4.0 applies to the abess article; GPL-3 applies to the abess software. Our corpus is the article.
12. **Is there data leakage?** Questions and answers are not indexed. However, the public paper may have been part of the LLM's training data, which we cannot inspect. Closed-book is a practical baseline, not a test of entirely unseen knowledge.
13. **Is the gold set exhaustive?** No. Equivalent passages may fall outside selected spans. This limitation is disclosed, and generation review inspects actual context.
14. **Why not use the original Chroma store?** With a few dozen chunks, exhaustive normalized dot products are sufficient and easy to inspect. The prototype's default distance should not be assumed identical to the experiment's cosine.
15. **How should documents be updated?** Track versions and hashes, rebuild extraction/chunks/index after changes, remove stale chunks, and rerun regression checks. Historical questions retain the 2022 snapshot.
16. **Are the RAG-Sequence example probabilities measured?** No. They are explicitly hypothetical teaching values. The API logs do not provide those conditional sequence probabilities.
17. **Who graded the answers?** An AI assistant checked them against sources and prompts. There is no independent blind multi-rater evaluation. Phan Anh Khoa and Bùi Trọng Thành have both reviewed and accepted the labels.
18. **Would 20/20 correct establish a hallucination-free model?** No. It would describe only the observed questions under the stated rubric and run conditions, not a guarantee for other questions.
