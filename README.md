# AppraisalAI

**Commercial real estate (CRE) narrative generator** — ingest a property parcel identifier and produce a localized, compliance-oriented draft for **Market Area Analysis** and **Highest and Best Use** sections of commercial appraisals.

## Problem and approach

Appraisers spend hours assembling narrative from scattered public and proprietary sources. This platform treats **retrieved data as the source of truth** and uses LLMs only to **summarize and structure** that evidence (RAG-style), not to invent zoning, demographics, or valuations.

## Repository layout

| Path | Purpose |
|------|---------|
| `src/appraisal_ai/` | Python application package (API clients, orchestration, prompts). |
| `config/` | Non-secret defaults; local overrides via environment. |
| `docs/` | API catalogs, compliance notes, runbooks. |
| `scripts/` | One-off utilities (data dictionary normalization, smoke tests). |
| `tests/` | Pytest suite. |
| `build.gradle` | Build automation hooks (env checks, asset prep before deploy). |

## Prerequisites

- **Python 3.11+** (3.12 recommended).
- **Mamba** or **Conda** — isolated env for scraping, geodata, and ML/LLM stacks. See `environment.yml`.
- **JDK 17+** if you use Gradle tasks locally.
- macOS ARM64 is a supported dev target; production can differ.

## Quick start

```bash
# Create and activate the conda/mamba environment
mamba env create -f environment.yml
mamba activate appraisal-ai

# Install the package in editable mode with dev deps
pip install -e ".[dev]"

# Copy env template and fill secrets (never commit .env)
cp config/env.example .env

# Run tests
pytest
```

Optional Gradle (from repo root):

```bash
gradle checkPythonEnv   # sanity check; extend in build.gradle
```

## Configuration

- **Secrets**: use `.env` (see `config/env.example`). Do not commit API keys or CoStar credentials.
- **Data dictionaries**: place normalized field maps under `config/`; Gradle or `scripts/` can sync names before deploy.

## Product guardrails

- Do **not** use the model for arithmetic, value conclusions, or facts not present in retrieved context.
- Log provenance (source API + retrieval timestamp) for auditability.
- Human review remains the default before bank submission.

## Documentation

- [External APIs useful for CRE narratives](docs/API_REFERENCE.md)

## License

Proprietary — assign a license before open-sourcing any portion.



https://singlefamily.fanniemae.com/news-events/updated-uad-redesign-timeline-specific-implementation-dates
https://singlefamily.fanniemae.com/media/40731/display
https://singlefamily.fanniemae.com/media/25391/display
https://singlefamily.fanniemae.com/delivering/uniform-mortgage-data-program/uniform-appraisal-dataset
https://singlefamily.fanniemae.com/media/44506/display