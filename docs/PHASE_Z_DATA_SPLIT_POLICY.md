# Phase Z — Data Split & Benchmark Leakage Protection Policy (`docs/PHASE_Z_DATA_SPLIT_POLICY.md`)

## 1. Objective & Policy Governance

This policy governs data splits and leakage protection for **Phase Z — Offline Domain-Specific Dense Embedding Fine-Tuning & Hard Negative Mining**.

To preserve the scientific integrity and evaluation authority of ContextIQ, the 30 official benchmark test cases in [`evaluation/benchmark_dataset.py`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/evaluation/benchmark_dataset.py) are designated as a **PROTECTED FINAL TEST SET**.

---

## 2. Strict One-Way Data Flow Architecture

The data pipeline strictly enforces a **one-way data flow**. Zero information from the protected test set may flow backwards into training, negative mining, validation split selection, model checkpointing, or hyperparameter tuning:

```
[ Enterprise Corpus (182 Chunks / Raw Docs / Ontology Graph) ]
                         │
                         ▼  (Excludes 30 Protected Benchmark Questions)
[ Triplet Generation Engine (scratch/build_phase_z_training_pairs.py) ]
                         │
                         ▼  (Deterministic Semantic Family Split)
             ┌───────────┴───────────┐
             ▼                       ▼
    [ Training Set (80%) ]   [ Held-out Validation Set (20%) ]
             │                       │
             ▼                       ▼
    [ Contrastive Training ]  [ Margin & Retrieval Pre-Evaluation ]
             │                       │
             └───────────┬───────────┘
                         ▼
        [ Freeze Model Checkpoint (artifacts/phase_z/) ]
                         │
                         ▼  (Single Blind Final Test - ZERO Retries)
        [ Protected 30-Case Benchmark (BenchmarkEvaluator) ]
```

---

## 3. Explicit Data Leakage Safeguards

1. **Query Protection**: No benchmark question string from `BENCHMARK_TEST_CASES` may be parsed, embedded, or transformed into a training example.
2. **Document Exclusion Guard**: Triplet generation operates on non-benchmark query templates derived from enterprise document metadata and SHACL ontology relations.
3. **Chunk/Entity Grouping**: Near-duplicate document chunks belonging to the same entity or process domain are assigned strictly to either the training split or the validation split to prevent chunk leakage across splits.
4. **Single-Blind Benchmark Evaluation**: The 30-case official benchmark is run **ONCE** on the final frozen checkpoint. Iterative hyperparameter tuning against the benchmark dataset is strictly prohibited.
