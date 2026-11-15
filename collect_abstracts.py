"""
How abstracts_cache.csv was created.

For every DOI in the SPICED dataset, the abstract is requested from the Semantic Scholar batch API.
DOIs without an abstract there are then requested from OpenAlex (the successor to Microsoft Academic Graph).
The notebook itself does not run this script; it loads the resulting abstracts_cache.csv from this repository.

Run (needs: pandas, pyarrow, requests):  python collect_abstracts.py
"""
import time

import pandas as pd
import requests

SPICED_URL = "https://huggingface.co/api/datasets/copenlu/spiced/parquet/default/{split}/0.parquet"


def fetch_semantic_scholar(dois, batch=400):
    """Abstracts from the Semantic Scholar batch API, retrying on rate limits."""
    found = {}
    for i in range(0, len(dois), batch):
        chunk = dois[i:i + batch]
        for attempt in range(8):
            r = requests.post(
                "https://api.semanticscholar.org/graph/v1/paper/batch",
                params={"fields": "title,abstract,year"},
                json={"ids": [f"DOI:{d}" for d in chunk]},
                timeout=90,
            )
            if r.status_code == 200:
                break
            time.sleep(min(60, 3 * 2 ** attempt))
        else:
            continue
        for doi, item in zip(chunk, r.json()):
            if item and item.get("abstract"):
                found[doi] = {"title": item.get("title"), "year": item.get("year"),
                              "abstract": item["abstract"], "abstract_source": "semantic_scholar"}
        time.sleep(1.5)
    return found


def fetch_openalex(dois, batch=40):
    """Abstracts from OpenAlex, which stores them as {word: [positions]}."""
    found = {}
    for i in range(0, len(dois), batch):
        params = {"filter": "doi:" + "|".join(dois[i:i + batch]), "per-page": 50,
                  "select": "doi,display_name,publication_year,abstract_inverted_index"}
        r = requests.get("https://api.openalex.org/works", params=params, timeout=90)
        if r.status_code != 200:
            continue
        for work in r.json().get("results", []):
            index = work.get("abstract_inverted_index")
            if not index:
                continue
            positions = {p: word for word, ps in index.items() for p in ps}
            doi = (work.get("doi") or "").replace("https://doi.org/", "").lower()
            found[doi] = {"title": work.get("display_name"), "year": work.get("publication_year"),
                          "abstract": " ".join(positions[p] for p in sorted(positions)),
                          "abstract_source": "openalex"}
        time.sleep(0.3)
    return found


if __name__ == "__main__":
    spiced = pd.concat([pd.read_parquet(SPICED_URL.format(split=s)) for s in ["train", "validation", "test"]])
    dois = sorted(spiced["DOI"].str.strip().str.lower().unique())

    abstracts = fetch_semantic_scholar(dois)
    print(f"Semantic Scholar: {len(abstracts)} / {len(dois)}")
    abstracts.update(fetch_openalex([d for d in dois if d not in abstracts]))
    print(f"After OpenAlex: {len(abstracts)} / {len(dois)}")

    pd.DataFrame([{"doi": d, **v} for d, v in abstracts.items()]).to_csv("abstracts_cache.csv", index=False)
    print("Saved abstracts_cache.csv")
