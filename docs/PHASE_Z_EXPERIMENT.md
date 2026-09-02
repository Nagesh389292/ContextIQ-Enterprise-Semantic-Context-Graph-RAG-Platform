# Phase Z — Fine-Tuning Experiment & Margin Progression Report (`docs/PHASE_Z_EXPERIMENT.md`)

## Executive Summary

Phase Z executed contrastive fine-tuning of `all-MiniLM-L6-v2` using MultipleNegativesRankingLoss on 428 enterprise triplets. Pre- and post-fine-tuning cosine margins were measured on 144 held-out validation triplets (grouped by semantic entity families) to evaluate semantic discrimination prior to protected benchmark testing.

---

## 1. Experimental Training Configuration

| Parameter | Value | Details |
|---|---|---|
| **Base Model** | `all-MiniLM-L6-v2` | SentenceTransformers 384-dim dense embedder |
| **Loss Function** | `MultipleNegativesRankingLoss` | Contrastive cross-entropy over batch negatives |
| **Optimizer** | `AdamW` | Learning rate `2e-5`, weight decay `0.01` |
| **Batch Size** | `16` | 16 triplets per batch |
| **Epochs** | `3` | Epoch 1 Loss: `2.5272` $\rightarrow$ Epoch 2 Loss: `1.5586` $\rightarrow$ Epoch 3 Loss: `1.1895` |
| **Checkpoint Path** | [`artifacts/phase_z/checkpoint`](file:///c:/Users/NAGESH%20REDDY/Desktop/SAP/enterprise-semantic-context-engine/artifacts/phase_z/checkpoint) | Frozen isolated experimental model |

---

## 2. Pre vs Post Validation Margin Progression

Measured on **144 held-out validation triplets** (zero entity overlap with training set):

| Validation Metric | Pre-Fine-Tuning (Control) | Post-Fine-Tuning (Phase Z) | Delta | Relative Gain |
|---|---:|---:|---:|---:|
| **Mean Positive Cosine Sim ($\cos_{pos}$)** | 0.4170 | 0.2703 | -0.1467 | Normalized compression |
| **Mean Hard Negative Cosine Sim ($\cos_{neg}$)** | 0.3939 | 0.1931 | -0.2008 | Strong negative pushback |
| **Mean Semantic Margin ($\Delta \cos$)** | **+0.0231** | **+0.0772** | **+0.0541** | **+234.2%** |
| **Median Semantic Margin** | +0.0079 | +0.0397 | +0.0318 | +402.5% |
| **25th Percentile Margin** | -0.0581 | +0.0055 | +0.0636 | Negative margin eliminated |
| **75th Percentile Margin** | +0.0859 | +0.1582 | +0.0723 | +84.2% |
| **Positive Margin Rate ($\Delta \cos > 0$)** | **57.64%** | **79.86%** | **+22.22%** | **+38.5%** |
| **Collision Rate ($\Delta \cos < 0$)** | 42.36% | 20.14% | -22.22% | Reduced by half |

> [!NOTE]
> Fine-tuning successfully reduced semantic collisions on held-out domain validation data, increasing the positive margin rate from 57.64% to 79.86% and boosting mean cosine margin by +0.0541.
