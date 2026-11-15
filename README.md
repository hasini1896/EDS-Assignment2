# Dataset for reproducing "Information Retention in the Multi-Platform Sharing of Science"

Data files used by the EDS Assignment 2 notebook that reproduces:

> Hwang, S., Horvát, E.-Á., & Romero, D. M. (2023). *Information Retention in the Multi-Platform Sharing of Science*.
> Proceedings of ICWSM, 17(1), 375–386. https://doi.org/10.1609/icwsm.v17i1.22153

The notebook loads these files directly from this repository, so it runs quickly and does not depend on outside APIs.

## Files

| File | Rows | Description | Original source |
|---|---|---|---|
| `spiced_train.parquet` | 4,721 | SPICED training split | [Hugging Face: copenlu/spiced](https://huggingface.co/datasets/copenlu/spiced) |
| `spiced_validation.parquet` | 664 | SPICED validation split | same |
| `spiced_test.parquet` | 640 | SPICED test split | same |
| `abstracts_cache.csv` | 1,925 | Abstracts of the papers cited in SPICED (columns: `doi`, `title`, `year`, `abstract`, `abstract_source`) | [Semantic Scholar API](https://api.semanticscholar.org/) and [OpenAlex](https://openalex.org/) |
| `example_abstract.csv` | 1 | Abstract of the paper's own example article (DOI 10.1016/j.ctrv.2016.11.010), used for a sanity check | Semantic Scholar API |
| `collect_abstracts.py` | – | Script that created `abstracts_cache.csv` | – |

**SPICED** pairs a finding stated in a news article or tweet with the finding from the scientific paper it reports on.
Each pair is rated by human annotators from 1 (different information) to 5 (same information).
The files are unmodified copies of the original Parquet files.

**Abstracts** were downloaded by DOI from Semantic Scholar, with OpenAlex as a fallback for DOIs Semantic Scholar did not cover
(see `collect_abstracts.py`). The `abstract_source` column records which service each abstract came from.

## Licences and credit

- SPICED: MIT licence, Copyright (c) 2022 CopeNLU, BlaBlaLab. See `LICENSE_SPICED.txt`.
  Please cite: Wright, D., Pei, J., Jurgens, D., & Augenstein, I. (2022). *Modeling Information Change in Science Communication
  with Semantically Matched Paraphrases*. EMNLP 2022.
- Abstracts: collected through the Semantic Scholar API and OpenAlex (OpenAlex data is CC0). The abstract text remains the
  property of the original publishers and is shared here only for non-commercial academic coursework.
