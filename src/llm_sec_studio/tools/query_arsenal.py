#!/usr/bin/env python3
"""
tools/query_arsenal.py — On-demand curated RAG router across WSF, Centinela, and StreamerBot.
Strictly enforces domain allowlists, excludes entertainment/casino noise, and bounds output <= 1500 tokens.
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = ROOT / "config" / "arsenal_registry.json"
SHARED_WSF_ROOT = Path(os.environ.get("WSF_SHARED_ROOT", "C:/Users/tomas/Desktop/web-software-factory"))
RAG_CACHE_DIR = Path(os.environ.get("ARSENAL_RAG_CACHE_DIR", str(SHARED_WSF_ROOT / ".cache")))


def est_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4)


def load_registry() -> dict:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def is_excluded(path_or_text: str, exclude_patterns: list[str]) -> bool:
    low = path_or_text.lower()
    return any(pat in low for pat in exclude_patterns)


def extract_terms(query: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z0-9_]{2,}", query)
    dedup = []
    seen = set()
    for t in tokens:
        tl = t.lower()
        if tl not in seen:
            seen.add(tl)
            dedup.append(t)
    return dedup[:10]


def build_fts_query(terms: list[str], use_and: bool = True) -> str:
    if not terms:
        return ""
    joiner = " AND " if use_and else " OR "
    return joiner.join(f'"{t}"' for t in terms)


def query_sqlite_db(
    db_path: Path,
    source_label: str,
    allowed_domains: list[str],
    exclude_patterns: list[str],
    terms: list[str],
    limit: int,
    priority_boost: float,
) -> list[dict]:
    if not db_path.is_file() or not terms:
        return []
    hits = []
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        placeholders = ",".join("?" for _ in allowed_domains)
        for use_and in (True, False):
            fts_q = build_fts_query(terms, use_and=use_and)
            sql = f"""
                SELECT d.rel_path, d.title, d.domain, c.heading_path, c.text,
                       bm25(chunks_fts) AS rank
                FROM chunks_fts
                JOIN chunks c ON c.chunk_id = chunks_fts.rowid
                JOIN docs d ON d.doc_id = c.doc_id
                WHERE chunks_fts MATCH ?
                  AND d.domain IN ({placeholders})
                ORDER BY rank ASC
                LIMIT ?
            """
            rows = conn.execute(sql, [fts_q, *allowed_domains, limit * 3]).fetchall()
            if rows:
                for rel_path, title, dom, heading, text, rank in rows:
                    if is_excluded(rel_path or "", exclude_patterns) or is_excluded(title or "", exclude_patterns):
                        continue
                    score = max(0.1, (-float(rank))) + priority_boost + (2.0 if use_and else 0.0)
                    hits.append({
                        "source": source_label,
                        "domain": dom,
                        "path": rel_path,
                        "heading": heading or title or "",
                        "score": round(score, 3),
                        "text": (text or "").strip(),
                    })
                if len(hits) >= limit:
                    break
    finally:
        conn.close()
    return hits


def query_curated_files(
    file_paths: list[str],
    exclude_patterns: list[str],
    terms: list[str],
    domain: str,
    limit: int,
) -> list[dict]:
    if not terms:
        return []
    low_terms = [t.lower() for t in terms]
    hits = []
    expanded_paths: list[Path] = []
    for raw_path in file_paths:
        p = Path(raw_path)
        if not p.is_absolute():
            cand = ROOT / raw_path
            p = cand if cand.exists() else (SHARED_WSF_ROOT / raw_path)
        if p.is_dir():
            for child in sorted(p.rglob("*.md")):
                if child.is_file() and not is_excluded(str(child), exclude_patterns):
                    expanded_paths.append(child)
        elif p.is_file() and not is_excluded(str(p), exclude_patterns):
            expanded_paths.append(p)

    for p in expanded_paths:
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if p.suffix.lower() == ".json":
            # Scan JSON blocks cleanly by top-level chunks or lines
            lines = content.splitlines()
            window = 18
            step = 10
            for idx in range(0, len(lines), step):
                chunk = "\n".join(lines[idx : idx + window])
                clow = chunk.lower()
                matched = sum(1 for t in low_terms if t in clow)
                if matched > 0 and not is_excluded(clow, exclude_patterns):
                    hits.append({
                        "source": "curated_catalog",
                        "domain": domain,
                        "path": str(p),
                        "heading": f"lines {idx + 1}-{min(len(lines), idx + window)}",
                        "score": round(matched * 2.5 + 1.0, 3),
                        "text": chunk.strip(),
                    })
        else:
            rel_str = str(p.relative_to(ROOT)) if str(p).startswith(str(ROOT)) else str(p)
            fname_low = rel_str.lower()
            is_delta = "delta_docs_2026" in fname_low
            is_skill = "skills_library" in fname_low
            fname_matches = sum(1 for t in low_terms if t in fname_low)
            sections = re.split(r"(?m)^(?=#{1,3}\s)", content)
            for sec in sections:
                if len(sec.strip()) < 40:
                    continue
                slow = sec.lower()
                if is_excluded(slow, exclude_patterns):
                    continue
                matched = sum(1 for t in low_terms if t in slow)
                if matched > 0:
                    first_line = sec.splitlines()[0].lstrip("# ").strip()[:100]
                    heading_matches = sum(1 for t in low_terms if t in first_line.lower())
                    boost = (
                        (13.0 * fname_matches + 5.0)
                        if ((is_delta or is_skill) and fname_matches > 0)
                        else (3.0 if (is_delta or is_skill) else 0.0)
                    )
                    score = matched * 4.5 + heading_matches * 3.0 + boost
                    src_tag = "skills_library" if is_skill else ("delta_doc" if is_delta else "curated_doc")
                    hits.append({
                        "source": src_tag,
                        "domain": domain,
                        "path": rel_str,
                        "heading": first_line,
                        "score": round(score, 3),
                        "text": sec.strip(),
                    })
    hits.sort(key=lambda x: x["score"], reverse=True)
    return hits[: limit * 2]


def query_qdrant_optional(
    collections: list[str],
    exclude_patterns: list[str],
    terms: list[str],
    domain: str,
    limit: int,
) -> list[dict]:
    env_path = ROOT / ".env"
    if not env_path.is_file() or not collections or not terms:
        return []
    host, key = "", ""
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^\s*(QDRANT_HOST|QDRANT_API_KEY)\s*=(.*)$", line)
        if m:
            val = m.group(2).strip().strip('"').strip("'")
            if m.group(1) == "QDRANT_HOST":
                host = val.rstrip("/")
            else:
                key = val
    if not host or not key:
        return []

    low_terms = [t.lower() for t in terms]
    hits = []
    for col in collections:
        try:
            body = json.dumps({"limit": 60, "with_payload": True, "with_vector": False}).encode()
            req = urllib.request.Request(
                f"{host}/collections/{col}/points/scroll",
                data=body,
                headers={"api-key": key, "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=6) as resp:
                pts = json.loads(resp.read().decode()).get("result", {}).get("points", [])
            for pt in pts:
                pl = pt.get("payload") or {}
                src = str(pl.get("source") or pl.get("source_file") or "")
                txt = str(pl.get("text") or "")
                if is_excluded(src, exclude_patterns) or is_excluded(txt, exclude_patterns):
                    continue
                tlow = (src + " " + txt).lower()
                matched = sum(1 for t in low_terms if t in tlow)
                if matched > 0:
                    hits.append({
                        "source": f"qdrant:{col}",
                        "domain": domain,
                        "path": src,
                        "heading": str(pl.get("heading") or pl.get("header_path") or pl.get("title") or ""),
                        "score": round(matched * 1.8, 3),
                        "text": txt.strip(),
                    })
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as err:
            print(f"[query_arsenal] qdrant skip {col}: {err}", file=sys.stderr)
    hits.sort(key=lambda x: x["score"], reverse=True)
    return hits[:limit]


def bound_results(hits: list[dict], top_k: int, max_tokens: int) -> list[dict]:
    # Deduplicate by (path, heading) keeping highest score
    deduped = {}
    for h in sorted(hits, key=lambda x: x["score"], reverse=True):
        key = (h["path"], h["heading"])
        if key not in deduped:
            deduped[key] = h

    selected = []
    remaining_tokens = max(200, max_tokens - 90)
    per_chunk_cap_tokens = max(180, remaining_tokens // max(1, top_k))

    for h in list(deduped.values())[:top_k]:
        max_chars = min(per_chunk_cap_tokens * 4, remaining_tokens * 4)
        if max_chars < 120:
            break
        txt = h["text"]
        if len(txt) > max_chars:
            txt = txt[: max_chars - 3].rsplit(" ", 1)[0] + "..."
        tok = est_tokens(txt) + 25
        remaining_tokens -= tok
        selected.append({
            "source": h["source"],
            "domain": h["domain"],
            "path": h["path"],
            "heading": h["heading"],
            "score": h["score"],
            "tokens_est": tok,
            "excerpt": txt,
        })
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description="Query curated multi-project RAG arsenal.")
    parser.add_argument("positional_query", nargs="?", default="", help="Search query")
    parser.add_argument("-q", "--query", dest="opt_query", default="", help="Search query")
    parser.add_argument(
        "-d", "--domain",
        default="all",
        choices=["all", "cybersec_audit", "agent_harness", "web_engineering", "browser_automation"],
        help="Target curated domain",
    )
    parser.add_argument("--top-k", type=int, default=3, help="Max chunks to return (default: 3)")
    parser.add_argument("--max-tokens", type=int, default=1500, help="Hard output token budget (default: 1500)")
    parser.add_argument("--qdrant", action="store_true", help="Include Qdrant Cloud scroll filter")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--list-domains", action="store_true", help="List curated domains and exit")
    args = parser.parse_args()

    reg = load_registry()
    if args.list_domains:
        out = {k: v["summary"] for k, v in reg["domains"].items()}
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    query = (args.opt_query or args.positional_query).strip()
    if not query:
        parser.error("Provide --query '<text>' or positional query.")

    terms = extract_terms(query)
    exclude_patterns = reg.get("exclude_patterns", [])
    domains_to_search = list(reg["domains"].keys()) if args.domain == "all" else [args.domain]

    sqlite_domains = []
    curated_files = []
    qdrant_cols = []
    for d in domains_to_search:
        cfg = reg["domains"][d]
        sqlite_domains.extend(cfg.get("sqlite_domains", []))
        curated_files.extend(cfg.get("catalogs", []))
        curated_files.extend(cfg.get("curated_docs", []))
        qdrant_cols.extend(cfg.get("qdrant_collections", []))

    sqlite_domains = sorted(set(sqlite_domains))
    curated_files = list(dict.fromkeys(curated_files))
    qdrant_cols = list(dict.fromkeys(qdrant_cols))

    hot_db = RAG_CACHE_DIR / Path(reg["stores"]["wsf_hot_sqlite"]).name
    lib_db = RAG_CACHE_DIR / Path(reg["stores"]["wsf_library_sqlite"]).name

    hits = []
    hits.extend(query_sqlite_db(hot_db, "wsf_hot_sqlite", sqlite_domains, exclude_patterns, terms, args.top_k, 1.5))
    hits.extend(query_curated_files(curated_files, exclude_patterns, terms, args.domain, args.top_k))
    if len(hits) < args.top_k * 2:
        hits.extend(query_sqlite_db(lib_db, "wsf_library_sqlite", sqlite_domains, exclude_patterns, terms, args.top_k, 0.5))
    if args.qdrant and qdrant_cols:
        hits.extend(query_qdrant_optional(qdrant_cols, exclude_patterns, terms, args.domain, args.top_k))

    bounded = bound_results(hits, max(1, min(args.top_k, 5)), min(args.max_tokens, 1500))
    payload = {
        "query": query,
        "domain": args.domain,
        "returned": len(bounded),
        "total_tokens_est": sum(r["tokens_est"] for r in bounded),
        "results": bounded,
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for idx, r in enumerate(bounded, 1):
            print(f"[{idx}] ({r['source']} | {r['domain']} | score={r['score']}) {r['path']} :: {r['heading']}")
            print(r["excerpt"])
            print("-" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
