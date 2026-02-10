#!/usr/bin/env python3
"""
API reranker for passage re-ranking after BM25 pre-filtering.
Zero external dependencies — uses only Python stdlib.

Supports: ZeroEntropy, Cohere, Voyage AI, Jina AI.

Usage:
    echo '{"query": "...", "passages": [...], "top_n": 20}' | python scripts/rerank.py

Input:  JSON with "query" string + "passages" array (BM25 output format: [{text, score, index}])
        Optional "top_n" (default 20)
Output: JSON array of top-N passages reranked, same format, with "rerank_score" added

Config via env vars:
    RERANKER_PROVIDER  = zerank|cohere|voyage|jina  (default: zerank)
    RERANKER_API_KEY   = <key>                       (required)
    RERANKER_MODEL     = <model>                     (optional, per-provider defaults)
    RERANKER_TIMEOUT   = <seconds>                   (default: 5)

On any error, passes BM25 input unchanged to stdout + warning to stderr.
"""

import json
import os
import sys
import urllib.request
import urllib.error

# --- Provider Configuration ---
PROVIDERS = {
    "zerank": {
        "endpoint": "https://api.zeroentropy.dev/v1/models/rerank",
        "model": "zerank-2",
        "top_n_field": "top_n",
        "results_field": "results",
    },
    "cohere": {
        "endpoint": "https://api.cohere.com/v2/rerank",
        "model": "rerank-v4.0-pro",
        "top_n_field": "top_n",
        "results_field": "results",
    },
    "voyage": {
        "endpoint": "https://api.voyageai.com/v1/rerank",
        "model": "rerank-2.5",
        "top_n_field": "top_k",
        "results_field": "data",
    },
    "jina": {
        "endpoint": "https://api.jina.ai/v1/rerank",
        "model": "jina-reranker-v2-base-multilingual",
        "top_n_field": "top_n",
        "results_field": "results",
    },
}

DEFAULT_TOP_N = 20
DEFAULT_TIMEOUT = 5


def rerank(query, passages, top_n, provider, api_key, model, timeout):
    """Call reranker API and return reranked passages."""
    config = PROVIDERS[provider]
    used_model = model or config["model"]

    body = {
        "model": used_model,
        "query": query,
        "documents": [p["text"] for p in passages],
        config["top_n_field"]: min(top_n, len(passages)),
    }

    req = urllib.request.Request(
        config["endpoint"],
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    resp = urllib.request.urlopen(req, timeout=timeout)
    data = json.loads(resp.read())
    results = data[config["results_field"]]

    # Map back to passage objects, sorted by rerank score descending
    ranked = sorted(results, key=lambda r: r["relevance_score"], reverse=True)
    return [
        {**passages[r["index"]], "rerank_score": round(r["relevance_score"], 4)}
        for r in ranked
    ]


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    # Read input from stdin
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"reranker: invalid JSON input: {e}", file=sys.stderr)
        sys.stdout.write(raw)
        sys.exit(0)

    query = data.get("query", "")
    passages = data.get("passages", [])
    top_n = data.get("top_n", DEFAULT_TOP_N)

    # If no passages, pass through
    if not passages:
        json.dump(passages, sys.stdout, indent=2)
        print()
        return

    # Read config from env
    api_key = os.environ.get("RERANKER_API_KEY", "")
    provider = os.environ.get("RERANKER_PROVIDER", "zerank").lower()
    model = os.environ.get("RERANKER_MODEL", "")
    timeout = int(os.environ.get("RERANKER_TIMEOUT", str(DEFAULT_TIMEOUT)))

    # No API key → pass through BM25 output unchanged
    if not api_key:
        print("reranker: RERANKER_API_KEY not set, passing through BM25 output", file=sys.stderr)
        json.dump(passages, sys.stdout, indent=2)
        print()
        return

    # Validate provider
    if provider not in PROVIDERS:
        print(f"reranker: unknown provider '{provider}', expected one of: {', '.join(PROVIDERS)}. Falling back.", file=sys.stderr)
        json.dump(passages, sys.stdout, indent=2)
        print()
        return

    # Attempt reranking with full fallback
    try:
        result = rerank(query, passages, top_n, provider, api_key, model, timeout)
        json.dump(result, sys.stdout, indent=2)
        print()
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()[:200]
        except Exception:
            pass
        print(f"reranker: HTTP {e.code} from {provider}: {body}. Falling back to BM25.", file=sys.stderr)
        json.dump(passages, sys.stdout, indent=2)
        print()
    except urllib.error.URLError as e:
        print(f"reranker: connection error ({provider}): {e.reason}. Falling back to BM25.", file=sys.stderr)
        json.dump(passages, sys.stdout, indent=2)
        print()
    except Exception as e:
        print(f"reranker: unexpected error: {e}. Falling back to BM25.", file=sys.stderr)
        json.dump(passages, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
