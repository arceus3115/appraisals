# `vendor/uad`

Optional local copies of GSE UAD documentation used to regenerate field mapping tables.

1. Download the current **Appendix G** (and related tables) from the [Fannie UAD page](https://singlefamily.fanniemae.com/delivering/uniform-mortgage-data-program/uniform-appraisal-dataset) or [Freddie UAD page](https://sf.freddiemac.com/tools-learning/uniform-mortgage-data-program/uad).
2. Save as `appendix_g.xlsx` (or adjust the path in `scripts/build_uad_mapping_from_vendor.py`).
3. Record the document revision in `VERSION.txt`.
4. Run:

```bash
python scripts/build_uad_mapping_from_vendor.py
```

If `appendix_g.xlsx` is absent, the script exits successfully without overwriting the committed starter CSV in `src/appraisal_ai/uad/data/`.

See [SOURCES.md](SOURCES.md) for canonical URLs.
