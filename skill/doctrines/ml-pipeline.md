---
name: ml-pipeline
version: 1.0.0
applies_to: [ml, training, inference, data-engineering]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: ml-pipeline v1.0.0

> Doctrine for ML training and inference pipelines. Reproducibility, dataset versioning, experiment tracking, GPU-cost discipline, model lineage. Loaded by `.bequite/bequite.config.toml::doctrines = ["ml-pipeline"]`.

## 1. Scope

Projects that train, fine-tune, evaluate, or serve ML models. Includes data preprocessing pipelines, training scripts, evaluation harnesses, model registries, and inference servers. Stacks: PyTorch, TensorFlow, JAX, Transformers, scikit-learn, XGBoost, vLLM, llama.cpp.

**Does NOT cover:** the *application* that calls a trained model (use `default-web-saas` or `cli-tool` for the consuming application). LLM-application-only projects without training (use `default-web-saas` + a small ML config block).

## 2. Rules

### Rule 1 — Reproducible training runs
**Kind:** `block`
**Statement:** Every training run MUST be reproducible from: code commit SHA, dataset version (DVC / lakeFS / hash), config file (Hydra / OmegaConf / YAML), and seed (Python `random`, NumPy, PyTorch, CUDA). The training receipt records all of these.
**Check:** `bequite audit` parses training scripts; flags missing seed-setting or absent dataset-version pin.
**Why:** non-reproducible training is research-grade junk; production-grade ML is reproducible by definition.

### Rule 2 — Dataset versioning
**Kind:** `block`
**Statement:** Every training dataset is versioned. Approved patterns: **DVC** (data + git), **lakeFS** (object-store branching), **Pachyderm**, or content-addressable storage (data hash → S3 path). Raw filesystem paths to mutable datasets are forbidden.
**Check:** `bequite audit` parses data-loader code; flags `pd.read_csv("/path/to/data.csv")` patterns without a version.
**Why:** training drift from "the file moved" is the #1 silent ML bug.

### Rule 3 — Experiment tracking
**Kind:** `recommend`
**Statement:** Every training run logs metrics + hyperparameters + artifacts to an experiment tracker. Approved options: **Weights & Biases** (hosted), **MLflow** (self-hosted), **Aim** (open-source), **Neptune** (hosted). The tracker's run-id is included in the BeQuite receipt.
**Check:** advisory; the receipt entry is required.
**Why:** without tracking, "which model is in production?" becomes unanswerable.

### Rule 4 — GPU-cost ceiling per run
**Kind:** `block`
**Statement:** Every training script reads `BEQUITE_TRAINING_COST_USD` from env / config and aborts if cost projection exceeds it. Cost projection: `(throughput_samples_per_second × dataset_size × epochs ÷ 3600) × hourly_GPU_rate`.
**Check:** `bequite verify` planted-test asserts the abort fires when ceiling is small.
**Why:** runaway training jobs are catastrophic.

### Rule 5 — Model lineage
**Kind:** `block`
**Statement:** Every saved model artifact carries metadata: training-run-id, dataset-version, parent-model-id (for fine-tuning), git-commit, BeQuite-receipt-sha. Stored as `model.lineage.json` alongside the weights.
**Check:** `bequite audit` parses `*.safetensors` / `*.pt` / `*.bin` / `*.gguf` directories; flags missing `lineage.json`.
**Why:** model recall (a CVE in a base model, a poisoned dataset finding) requires lineage.

### Rule 6 — Eval before deploy
**Kind:** `block`
**Statement:** No model is deployed without an eval suite passing. The eval suite includes: a held-out set with documented thresholds, regression-test set (samples that previously failed and were fixed), red-team set (adversarial / safety samples).
**Check:** `bequite verify` runs the eval suite; deploys gated on green.
**Why:** "the loss looked low so I shipped it" is malpractice.

### Rule 7 — No PII in training data without DPIA
**Kind:** `block`
**Statement:** Training data containing PII / PHI / regulated data requires a documented DPIA (Data Protection Impact Assessment) and an ADR. Anonymisation strategy must be specified.
**Check:** `bequite audit` checks for the DPIA artifact when PII is declared in `dataset-card.md`.
**Why:** GDPR / HIPAA compliance.

### Rule 8 — Inference: input + output validation
**Kind:** `block`
**Statement:** Inference endpoints validate input shape / type / range BEFORE forward pass. Outputs are validated for NaN / Inf / out-of-range. Failed validation returns 4xx with a clear message; never crashes the worker.
**Check:** `bequite audit` parses inference code; flags raw forward-pass without validation.
**Why:** crash-on-bad-input takes down the model server for everyone.

### Rule 9 — Quantisation / distillation traceability
**Kind:** `recommend`
**Statement:** When a model is quantised (FP16 → INT8 / INT4) or distilled, the resulting model carries the parent-model-id and the conversion config. Eval on the quantised model is required (it's a different model).
**Check:** advisory; `bequite audit` greps for quantisation calls.
**Why:** quantisation can degrade quality silently; eval prevents shipping junk.

### Rule 10 — No `.env` in training data
**Kind:** `block`
**Statement:** Training data MUST NOT contain `.env` files, secrets, API keys, or other credential-shaped strings. Pre-training scan + post-training memorisation eval.
**Check:** `bequite audit` scans the dataset; trains a small probe model to detect if the model emits any planted secret string.
**Why:** OWASP LLM Top 10 (LLM07 — System Prompt Leakage; data poisoning).

### Rule 11 — No automated retraining without approval
**Kind:** `block`
**Statement:** Auto-retraining triggered by data drift / time / events MUST pause for human approval before promoting the new model. The approval is recorded in the receipt.
**Check:** `bequite audit` parses CI/CD; flags auto-promote-without-approval patterns.
**Why:** unsupervised model retraining is how models go silently bad.

### Rule 12 — Model card on every release
**Kind:** `block`
**Statement:** Every released model ships a Model Card (Mitchell et al. 2019) covering: intended use, training data, evaluation results per slice, ethical considerations, known failure modes, recommended threshold.
**Check:** `bequite audit` checks for `MODEL_CARD.md` per release tag.
**Why:** responsible ML.

## 3. Stack guidance

### Frameworks
| Choice | When |
|---|---|
| PyTorch | Default for research + most production |
| Transformers (HF) | LLM / NLP work |
| JAX | TPU-heavy, research |
| TensorFlow | Legacy + edge (TF Lite) |
| scikit-learn | Tabular / classical ML |
| XGBoost / LightGBM | Tabular at scale |

### Data + tracking
| Choice | When |
|---|---|
| DVC | Git-native dataset versioning |
| lakeFS | Object-store branching |
| Weights & Biases | Hosted experiment tracking |
| MLflow | Self-hosted + model registry |
| Aim | Open-source, local-first |

### Inference servers
| Choice | When |
|---|---|
| vLLM | LLM serving at scale |
| llama.cpp | CPU / Apple Silicon LLM |
| TorchServe | PyTorch general |
| BentoML | Multi-framework |
| Triton | NVIDIA stacks |
| KServe | Kubernetes-native |

### Hardware budgeting
- **Spot GPUs** (AWS / Lambda / RunPod / Vast.ai) for non-critical training.
- **Reserved GPUs** for production inference + critical training.
- **Apple M-series** for prototyping at zero variable cost.

## 4. Verification

`bequite verify` for ML projects:

1. **Reproduction smoke** — re-run the latest training script with the recorded seed; assert the model checkpoint hash matches (when bitwise reproduction is feasible) or that eval metrics are within ±0.5%.
2. **Eval suite** — run held-out + regression + red-team; assert all pass thresholds.
3. **Inference round-trip** — load the saved model, run a fixed input set, assert output matches recorded baseline.
4. **Dataset-version pin** — assert the recorded dataset version is reachable.
5. **Model card present + valid** — `MODEL_CARD.md` exists per release; sections are non-empty.
6. **No PII memorisation** — probe with planted-secret strings; assert model does NOT emit them.

## 5. Examples and references

- DVC: https://dvc.org/
- lakeFS: https://lakefs.io/
- Weights & Biases: https://wandb.ai/
- MLflow: https://mlflow.org/
- Aim: https://aimstack.io/
- vLLM: https://vllm.ai/
- Model Cards (Mitchell et al. 2019): https://arxiv.org/abs/1810.03993
- OWASP LLM Top 10 2025: https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/

## 6. Forking guidance

Common forks:
- **`ml-pipeline-research`** — relax Rule 1 (reproducibility) to "best-effort," drop Rule 11 (auto-retrain approval).
- **`ml-pipeline-edge`** — add edge-deployment rules (model size ceiling, quantisation required).
- **`ml-pipeline-llm-fine-tune`** — add LLM-specific rules (RLHF / DPO discipline, evaluator agreement, refusal-rate tracking).

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: ml-pipeline@1.0.0`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–12 ratified.
```
