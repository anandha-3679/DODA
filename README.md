# DODA — Decoupled-Operator Driven Architecture

**A configurable framework for integrating domain knowledge into machine-learning feature selection.**

DODA is a research prototype designed to combine data-driven feature importance with domain-informed feature priorities. It aims to give clinicians and other domain experts greater control over which features are prioritized, while allowing researchers to evaluate the effect of those priorities on predictive performance.

The central research question is whether incorporating domain knowledge into feature selection can maintain predictive performance comparable to conventional feature selection.

> **Research status:** DODA is under development and requires systematic experimental validation. It is not a clinically validated decision-support system.

## 1. Motivation

Machine-learning feature selection typically prioritizes features according to statistical or model-derived criteria. However, the features considered important by a model may not always align with the priorities of clinicians or other domain experts.

DODA explores an alternative: combine mathematical feature scores with configurable domain-informed weights to produce a transparent, adjustable feature ranking.

The framework is intended to support:

- **Configurability:** Allow users to supply domain-informed feature weights.
- **Transparency:** Inspect mathematical scores, domain weights, and final fused scores.
- **Flexibility:** Support different feature-scoring operators and score-fusion strategies.
- **Predictive evaluation:** Test whether domain-informed prioritization affects downstream model performance.

## 2. How DODA Works

The current implementation follows a modular pipeline:

1. **Mathematical feature scoring:** Run one or more feature-scoring operators on the input data.
2. **Score aggregation:** Combine scores from multiple operators when an aggregation strategy is supplied.
3. **Score normalization:** Normalize the resulting mathematical feature scores.
4. **Domain-knowledge integration:** Retrieve feature weights from a configurable knowledge provider.
5. **Score fusion:** Combine mathematical scores with domain-informed weights.
6. **Feature selection:** Rank the fused scores and select the requested top-*K* features.

The framework returns intermediate and final scores to support inspection and comparison.

```text
Input Data
    |
    v
Mathematical Feature Scoring
    |
    v
Score Aggregation
    |
    v
Score Normalization
    |
    +----------------------+
    |                      |
    v                      v
Mathematical Scores   Domain-Informed Weights
    |                      |
    +----------+-----------+
               |
               v
          Score Fusion
               |
               v
        Final Feature Ranking
               |
               v
         Top-K Selection
```

## 3. Architecture

The repository separates the main responsibilities into modules.

| Module | Responsibility |
|---|---|
| `doda/selector.py` | Public scikit-learn-compatible selector interface |
| `doda/pipeline.py` | Orchestrates scoring, normalization, knowledge integration, and fusion |
| `doda/adapters/` | Adapters for feature-scoring implementations |
| `doda/aggregation/` | Aggregation of scores from multiple operators |
| `doda/knowledge/` | Domain-knowledge engine and weight providers |
| `doda/fusion/` | Mathematical and domain-informed score-fusion strategies |
| `doda/ranking/` | Top-*K* feature selection |
| `doda/utils/` | Input validation, preprocessing, and score normalization |
| `demo/` | Example clinical weights and demonstration notebook |

## 4. Domain-Knowledge Integration

DODA is designed to allow domain-informed priorities to be supplied separately from mathematical feature scores.

The repository currently includes a JSON example at `demo/clinical_weights.json`. It contains feature weights for a diabetes-related dataset.

These values are illustrative configuration inputs. They should not be interpreted as official WHO-assigned feature weights or as clinically validated estimates unless their sources and justification are independently established.

The intended workflow is to document the origin of each weight, make the weighting scheme configurable, and examine how different reasonable weighting choices affect feature rankings and predictive performance.

## 5. Score-Fusion Strategies

The current repository includes:

- **Hadamard fusion:** Combines corresponding mathematical scores and domain weights.
- **Rank fusion:** Combines mathematical and domain-informed feature ranks using reciprocal rank fusion.

The choice of fusion strategy can affect the final ordering of features. Their behavior and suitability should therefore be evaluated empirically rather than assumed to be interchangeable.

## 6. Installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/anandha-3679/DODA.git
cd DODA
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies and the local package:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## 7. Explore the Demonstration

Open `demo/demo_doda.ipynb` in Jupyter Notebook or Visual Studio Code to explore the current demonstration.

The example configuration is available at `demo/clinical_weights.json`.

The notebook is the starting point for understanding the current implementation. The public API, configuration format, and supported combinations of operators and fusion strategies may evolve as the research protocol is finalized.

## 8. Research Evaluation Plan

The framework's central scientific claim must be evaluated through controlled experiments.

The planned evaluation will investigate:

1. **Predictive performance:** Compare DODA with conventional feature selection using matched datasets, models, feature counts, and evaluation splits.
2. **Non-inferiority:** Determine whether predictive performance remains within a predefined acceptable margin relative to the unweighted baseline.
3. **Configurability:** Test whether changing domain-informed weights produces understandable changes in feature rankings.
4. **Robustness:** Examine sensitivity to alternative weight configurations and fusion strategies.
5. **Reproducibility:** Use a leakage-controlled evaluation pipeline with feature selection and data-dependent preprocessing performed within each training fold.
6. **Transparency:** Report intermediate scores, final rankings, and the rationale and sources for domain-informed weights.

The non-inferiority margin, primary metric, comparison methods, and statistical analysis must be defined before the final comparative evaluation.

## 9. Current Limitations

DODA is a research prototype. The following issues require attention before drawing conclusions about its effectiveness:

- Domain-informed weights need documented sources and a defensible rationale.
- Predictive non-inferiority has not been established by the presence of the framework alone.
- The effects of different weighting schemes and fusion strategies require systematic testing.
- The evaluation pipeline must be checked for data leakage and reproducibility.
- Performance across datasets does not, by itself, establish clinical utility or safety.

DODA should not be used to make patient-care decisions without appropriate validation and clinical oversight.

## 10. Intended Contribution

DODA explores a configurable approach to incorporating domain knowledge into feature prioritization while preserving the ability to inspect how that knowledge influences the final ranking.

Its intended contribution is not to assume that domain-informed feature selection is automatically better, but to provide a framework through which its effects can be explicitly controlled, examined, and evaluated.

## Repository

**GitHub:** https://github.com/anandha-3679/DODA

**License:** Not yet specified. Licensing should be added before the project is distributed for reuse.

