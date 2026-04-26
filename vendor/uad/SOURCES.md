# UAD vendor artifacts (version pinning)

Place **optional** machine-readable GSE downloads here so `scripts/build_uad_mapping_from_vendor.py` can normalize them into `src/appraisal_ai/uad/data/appendix_g_mapping.csv`.

Document the **edition date or revision** you imported in `VERSION.txt` (create when you add binaries).

## Primary references

| Resource | URL |
|----------|-----|
| Fannie Mae — Uniform Appraisal Dataset (UAD) hub | https://singlefamily.fanniemae.com/delivering/uniform-mortgage-data-program/uniform-appraisal-dataset |
| Freddie Mac — UAD | https://sf.freddiemac.com/tools-learning/uniform-mortgage-data-program/uad |
| Updated UAD redesign timeline (implementation dates) | https://singlefamily.fanniemae.com/news-events/updated-uad-redesign-timeline-specific-implementation-dates |
| Functioning without Form Numbers (legacy forms → URAR) | https://singlefamily.fanniemae.com/media/document/pdf/mapping-legacy-forms-redesigned-uniform-residential-appraisal-report-urar-property-type |
| UAD and Forms Redesign Timeline (PDF) | https://singlefamily.fanniemae.com/media/25391/display |
| UAD Lender Readiness Kit (PDF) | https://singlefamily.fanniemae.com/media/document/pdf/uad-lender-readiness-kit |

## Mapping spine (Appendix G)

The GSE **Appendix G — Redesign to Legacy UAD Cross-reference Guide** is listed on the Fannie/Freddie UAD pages. Export or save the vendor spreadsheet/PDF edition you used into this directory (e.g. `appendix_g.xlsx`) and run the build script documented in [README.md](README.md).

## Legacy UAD 2.6

Legacy specification, appendices (forms mapping, field rules), and compliance rules are linked from the same UAD hub under **UAD 2.6 and Resources**.

## UAD 3.6 samples

Appendix D sample scenarios and XML (Fannie/Freddie UAD documentation bundle) are the preferred source for golden tests. Redistribution may be restricted; use `tests/fixtures/uad/` for **synthetic** minimal XML unless your counsel approves committing GSE samples.

## License / redistribution

GSE PDFs and spreadsheets are subject to Fannie Mae / Freddie Mac terms of use. Do not commit large vendor binaries to git unless your organization permits it; this repo ships a **small starter mapping CSV** for development and tests.
