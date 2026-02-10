#!/usr/bin/env python3
"""
Citation graph expansion via Semantic Scholar API.
Zero external dependencies — uses only Python stdlib.

Usage:
    echo '{"urls": [...], "subquestion": "...", "top_n": 5}' | python scripts/citation_expand.py

Input:  JSON with "urls" (list of academic URLs), "subquestion" (string), optional "top_n" (default 5)
Output: JSON array of top-N papers from citation expansion, scored and ranked.

Config via env vars:
    S2_API_KEY   = <key>        (optional — uses unauth pool if not set)
    S2_TIMEOUT   = <seconds>    (default: 10)
    S2_MAX_SEEDS = <count>      (default: 3 — max seed papers to expand)

On any error, returns empty array to stdout + warning to stderr.
"""

import json
import math
import os
import re
import sys
import time
import urllib.request
import urllib.error

# --- Configuration ---
S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "paperId,title,year,citationCount,abstract,openAccessPdf,url"
S2_CITE_FIELDS = "paperId,title,year,citationCount,abstract,openAccessPdf,url,isInfluential"
DEFAULT_TOP_N = 5
DEFAULT_TIMEOUT = 10
DEFAULT_MAX_SEEDS = 3
RATE_LIMIT_DELAY = 1.1  # seconds between requests (slightly over 1 RPS)

# --- Academic URL patterns ---
ACADEMIC_PATTERNS = [
    (re.compile(r'arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5}(?:v\d+)?)'), 'arxiv'),
    (re.compile(r'arxiv\.org/(?:abs|pdf)/([a-z-]+/\d{7}(?:v\d+)?)'), 'arxiv'),
    (re.compile(r'doi\.org/(10\.\d{4,9}/[^\s"<>]+)'), 'doi'),
    (re.compile(r'pubmed\.ncbi\.nlm\.nih\.gov/(\d+)'), 'pubmed'),
    (re.compile(r'ncbi\.nlm\.nih\.gov/pmc/articles/(PMC\d+)'), 'pmc'),
    (re.compile(r'semanticscholar\.org/paper/[^/]*/([0-9a-f]{40})'), 's2'),
    (re.compile(r'dl\.acm\.org/doi/(10\.\d{4,9}/[^\s"<>]+)'), 'doi'),
    (re.compile(r'(?:bio|med)rxiv\.org/content/(10\.\d{4,9}/[^\s"<>]+)'), 'doi'),
]

STOPWORDS = frozenset([
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'she',
    'that', 'the', 'to', 'was', 'were', 'will', 'with', 'you', 'your',
    'this', 'they', 'but', 'have', 'had', 'what', 'when', 'where',
    'which', 'who', 'how', 'not', 'no', 'can', 'do', 'does', 'if',
    'than', 'then', 'so', 'we', 'our',
])


# --- ID Extraction ---
def extract_paper_id(url):
    """Extract S2-compatible paper ID from academic URL."""
    for pattern, source_type in ACADEMIC_PATTERNS:
        match = pattern.search(url)
        if match:
            raw_id = match.group(1)
            return _to_s2_id(raw_id, source_type), source_type
    return None, None


def _to_s2_id(raw_id, source_type):
    """Convert extracted ID to Semantic Scholar API format."""
    converters = {
        'arxiv': lambda x: f'ARXIV:{x}',
        'doi': lambda x: f'DOI:{x}',
        'pubmed': lambda x: f'PMID:{x}',
        'pmc': lambda x: f'PMCID:{x}',
        's2': lambda x: x,
    }
    converter = converters.get(source_type)
    return converter(raw_id) if converter else None


def _tokenize(text):
    """Simple tokenizer for keyword overlap scoring."""
    return {
        w for w in text.lower().split()
        if w not in STOPWORDS and len(w) > 2 and w.isalpha()
    }


# --- Scoring ---
def score_paper(paper, query_tokens, current_year=None):
    """Score a paper for relevance to the subquestion."""
    if current_year is None:
        current_year = time.localtime().tm_year

    score = 0.0

    # Citation count (log scale, capped at 4)
    cc = paper.get('citationCount') or 0
    if cc > 0:
        score += min(math.log10(cc + 1), 4.0)

    # Recency
    year = paper.get('year')
    if year:
        age = current_year - year
        if age <= 1:
            score += 3.0
        elif age <= 3:
            score += 2.0
        elif age <= 5:
            score += 1.0

    # Keyword overlap
    text = ((paper.get('title') or '') + ' ' + (paper.get('abstract') or '')).lower()
    text_tokens = _tokenize(text)
    overlap = len(query_tokens & text_tokens)
    score += min(overlap * 0.5, 3.0)

    # Influential citation bonus
    if paper.get('isInfluential'):
        score += 2.0

    # Open access bonus
    if paper.get('openAccessPdf'):
        score += 1.0

    # No abstract penalty
    if not paper.get('abstract'):
        score -= 1.0

    return round(score, 2)


# --- S2 API Client ---
class S2Client:
    """Minimal Semantic Scholar API client with rate limiting."""

    def __init__(self, api_key=None, timeout=DEFAULT_TIMEOUT):
        self.api_key = api_key
        self.timeout = timeout
        self._last_request = 0.0

    def _throttle(self):
        """Enforce rate limit."""
        elapsed = time.time() - self._last_request
        if elapsed < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - elapsed)
        self._last_request = time.time()

    def _get(self, path, params=None):
        """Make GET request to S2 API."""
        self._throttle()
        url = f"{S2_BASE}{path}"
        if params:
            query = '&'.join(f'{k}={urllib.request.quote(str(v))}' for k, v in params.items())
            url = f"{url}?{query}"

        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        req = urllib.request.Request(url, headers=headers)

        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("citation_expand: rate limited, backing off 5s", file=sys.stderr)
                time.sleep(5)
                self._last_request = time.time()
                try:
                    resp = urllib.request.urlopen(req, timeout=self.timeout)
                    return json.loads(resp.read())
                except Exception:
                    return None
            elif e.code == 404:
                return None
            else:
                print(f"citation_expand: HTTP {e.code} for {path}", file=sys.stderr)
                return None
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            print(f"citation_expand: network error: {e}", file=sys.stderr)
            return None

    def get_citations(self, paper_id, limit=100):
        """Get papers that cite this paper (forward)."""
        encoded_id = urllib.request.quote(paper_id, safe=':/')
        return self._get(f"/paper/{encoded_id}/citations", {
            "fields": S2_CITE_FIELDS,
            "limit": str(limit),
        })

    def get_references(self, paper_id, limit=100):
        """Get papers that this paper cites (backward)."""
        encoded_id = urllib.request.quote(paper_id, safe=':/')
        return self._get(f"/paper/{encoded_id}/references", {
            "fields": S2_CITE_FIELDS,
            "limit": str(limit),
        })


# --- Main Expansion ---
def expand_citations(urls, subquestion, top_n=DEFAULT_TOP_N, max_seeds=DEFAULT_MAX_SEEDS):
    """
    Expand citation graph from academic URLs.

    Args:
        urls: list of URLs (academic ones will be detected)
        subquestion: the research subquestion (for scoring)
        top_n: number of papers to return
        max_seeds: max seed papers to expand

    Returns:
        list of scored paper dicts, sorted by score descending
    """
    api_key = os.environ.get("S2_API_KEY", "")
    timeout = int(os.environ.get("S2_TIMEOUT", str(DEFAULT_TIMEOUT)))
    client = S2Client(api_key=api_key or None, timeout=timeout)

    query_tokens = _tokenize(subquestion)

    # Extract paper IDs from academic URLs
    seeds = []
    for url in urls:
        paper_id, source_type = extract_paper_id(url)
        if paper_id and len(seeds) < max_seeds:
            seeds.append((paper_id, url))

    if not seeds:
        return []

    print(f"citation_expand: expanding {len(seeds)} seed(s)", file=sys.stderr)

    # Expand each seed (citations + references)
    all_papers = {}  # paperId -> {paper, seed_count, direction, source_seed}

    for seed_id, seed_url in seeds:
        # Forward citations
        cites_data = client.get_citations(seed_id)
        if cites_data and 'data' in cites_data:
            for entry in cites_data['data']:
                paper = entry.get('citingPaper', {})
                pid = paper.get('paperId')
                if not pid:
                    continue
                if pid not in all_papers:
                    paper['isInfluential'] = entry.get('isInfluential', False)
                    all_papers[pid] = {
                        'paper': paper,
                        'seed_count': 1,
                        'direction': 'forward',
                        'source_seed': seed_id,
                    }
                else:
                    all_papers[pid]['seed_count'] += 1

        # Backward references
        refs_data = client.get_references(seed_id)
        if refs_data and 'data' in refs_data:
            for entry in refs_data['data']:
                paper = entry.get('citedPaper', {})
                pid = paper.get('paperId')
                if not pid:
                    continue
                if pid not in all_papers:
                    paper['isInfluential'] = entry.get('isInfluential', False)
                    all_papers[pid] = {
                        'paper': paper,
                        'seed_count': 1,
                        'direction': 'backward',
                        'source_seed': seed_id,
                    }
                else:
                    all_papers[pid]['seed_count'] += 1

    # Score and rank
    scored = []
    for pid, info in all_papers.items():
        paper = info['paper']
        base_score = score_paper(paper, query_tokens)

        # Seed overlap bonus
        if info['seed_count'] > 1:
            base_score += info['seed_count'] * 1.5

        scored.append({
            'paperId': pid,
            'title': paper.get('title', ''),
            'year': paper.get('year'),
            'citationCount': paper.get('citationCount', 0),
            'abstract': paper.get('abstract', ''),
            'url': paper.get('url') or f"https://www.semanticscholar.org/paper/{pid}",
            'openAccessPdf': (paper.get('openAccessPdf') or {}).get('url'),
            'score': round(base_score, 2),
            'source': f"{'citation_of' if info['direction'] == 'forward' else 'reference_of'}:{info['source_seed']}",
            'direction': info['direction'],
        })

    scored.sort(key=lambda x: x['score'], reverse=True)
    print(f"citation_expand: found {len(all_papers)} papers, returning top {min(top_n, len(scored))}", file=sys.stderr)
    return scored[:top_n]


# --- CLI Interface ---
def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    try:
        data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"citation_expand: invalid JSON input: {e}", file=sys.stderr)
        json.dump([], sys.stdout)
        print()
        return

    urls = data.get('urls', [])
    subquestion = data.get('subquestion', '')
    top_n = data.get('top_n', DEFAULT_TOP_N)

    if not urls:
        json.dump([], sys.stdout)
        print()
        return

    try:
        results = expand_citations(urls, subquestion, top_n=top_n)
        json.dump(results, sys.stdout, indent=2)
        print()
    except Exception as e:
        print(f"citation_expand: unexpected error: {e}", file=sys.stderr)
        json.dump([], sys.stdout)
        print()


if __name__ == '__main__':
    main()
