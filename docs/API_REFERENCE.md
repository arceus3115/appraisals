# External APIs and data sources for CRE narratives

Use this as a **starting catalog** for parcel enrichment, demographics, economics, and LLM calls. Always verify licensing, redistribution terms, and appraisal standards in your jurisdiction before production use.

## LLM orchestration (summarization only)

| Provider | Docs | Notes |
|----------|------|--------|
| OpenAI | [https://platform.openai.com/docs](https://platform.openai.com/docs) | Chat/completions, structured outputs; meter by token. |
| Anthropic | [https://docs.anthropic.com](https://docs.anthropic.com) | Claude; strong for long-context drafting from retrieved chunks. |

**Practice:** Ground every factual claim in retrieved JSON/text; store `source_id` + `fetched_at` alongside generated paragraphs.

## Parcel, ownership, and property attributes

| Source | Docs / portal | Notes |
|--------|----------------|--------|
| ATTOM Data | [https://api.developer.attomdata.com/docs](https://api.developer.attomdata.com/docs) | Property characteristics, sales, AVM-adjacent fields; common in proptech stacks. |
| Regrid | [https://regrid.com/api/](https://regrid.com/api/) | Nationwide parcel boundaries + many county attributes; paid tiers. |
| LightBox / CoreLogic (enterprise) | Vendor-specific | Common in lender workflows; contract-gated. |
| CoStar / LoopNet | Enterprise | Mentioned in your plan; typically **not** a self-serve HTTP API — integration is account- and contract-specific. |

**Practice:** Normalize parcel keys (FIPS + APN formats vary); keep a county-specific parser layer.

## Demographics and economy (public)

| Source | Docs | Notes |
|--------|------|--------|
| U.S. Census Bureau | [https://www.census.gov/data/developers/data-sets.html](https://www.census.gov/data/developers/data-sets.html) | ACS, Decennial, County Business Patterns — good for MSA/county narrative. |
| Bureau of Labor Statistics | [https://www.bls.gov/developers/](https://www.bls.gov/developers/) | Employment/unemployment series by area. |
| BEA | [https://apps.bea.gov/API/signup/index.cfm](https://apps.bea.gov/API/signup/index.cfm) | Regional GDP, personal income (macro context). |
| FRED (St. Louis Fed) | [https://fred.stlouisfed.org/docs/api/fred/](https://fred.stlouisfed.org/docs/api/fred/) | Economic time series; free API key. |

## Geography and geocoding

| Source | Docs | Notes |
|--------|------|--------|
| Census Geocoder | [https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html](https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html) | Free batch geocode → tie to Census geographies. |
| Mapbox Geocoding | [https://docs.mapbox.com/api/search/geocoding/](https://docs.mapbox.com/api/search/geocoding/) | Forward/reverse geocode; usage pricing. |
| Google Geocoding | [https://developers.google.com/maps/documentation/geocoding](https://developers.google.com/maps/documentation/geocoding) | Widely used; billing required. |

## Environmental and hazard context (disclosure-heavy)

| Source | Docs | Notes |
|--------|------|--------|
| EPA Envirofacts | [https://www.epa.gov/enviro/envirofacts_data_service_api](https://www.epa.gov/enviro/envirofacts_data_service_api) | Programmatic env program queries. |
| FEMA NFHL / OpenFEMA | [https://www.fema.gov/flood-maps/gis-data](https://www.fema.gov/flood-maps/gis-data) | Flood hazard layers; confirm local map adoption. |

## Zoning and land use

There is **no single national zoning API**. Typical patterns:

- County/city **open data portals** (Socrata, ArcGIS Hub) — zoning GIS + PDF code extracts.
- **Manual playbooks** per MSA: cache zoning district names and cite ordinance URLs in RAG context.

Document each MSA’s ingestion path under `docs/msa/` as you add coverage.

## HTTP client in this repo

Python code should prefer **`httpx`** for async-friendly calls and testability; wrap each vendor in a small client module under `src/appraisal_ai/clients/`.

## Compliance reminder

Generated text is **draft assistance**. Appraisers remain responsible for USPAP (or applicable standards), supervisory review, and lender requirements. Log data provenance and model version for defensibility.
