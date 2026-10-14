#!/usr/bin/env python3
"""Check this documentation release; not a clinical or anonymization certificate."""
import csv
import re
from pathlib import Path
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
expected = {
    "README.md", "AGENTS.md", ".gitignore",
    "docs/research-question.md", "docs/method-evolution.md",
    "docs/experiment-design.md", "docs/metric-definitions.md",
    "docs/results-and-analysis.md", "docs/failures-and-lessons.md",
    "docs/limitations-and-next-steps.md", "docs/provenance-and-scope.md",
    "results/README.md", "results/main_results.csv", "results/negative_control_proxy.csv",
    "memory/status.md", "memory/next.md", "memory/changelog.md",
    "tools/validate_publication.py",
}
files = {p.relative_to(root).as_posix(): p for p in root.rglob("*")
         if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts}
errors = []
if files.keys() != expected:
    errors.append(f"Unexpected file set: extra={files.keys() - expected}, missing={expected - files.keys()}")
patterns = [
    r"sk-[A-Za-z0-9_-]{20,}", r"gh[pousr]_[A-Za-z0-9_]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}", r"AKIA[A-Z0-9]{16}",
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"/(?:Users|root)/", r"\b(?:Case|case)\s+\d+",
    r"github\.com/[^/\s]+/medical(?:-archive)?(?:[)\s/]|$)",
]
for name, p in files.items():
    text = p.read_text(encoding="utf-8")
    if any(re.search(pattern, text) for pattern in patterns):
        errors.append("Sensitive-content pattern: " + name)
    if p.suffix == ".md":
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if "://" in link or link.startswith("#"):
                continue
            target = (p.parent / unquote(link.split("#")[0])).resolve()
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f"Broken or escaping link: {name} -> {link}")

def rows(name):
    with (root / "results" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

main = rows("main_results.csv")
neg = rows("negative_control_proxy.csv")
if [x["model"] for x in main] != ["A", "B", "C1-strict", "C2", "C3", "C3-filtered", "C4"]:
    errors.append("Unexpected main-result models")
article = (root / "docs/results-and-analysis.md").read_text(encoding="utf-8")
for row in main:
    fields = [row[k] or "—" for k in ("model", "keyword_count_proxy", "state_micro_f1", "report_micro_f1", "disagreement")]
    if "| " + " | ".join(fields) + " |" not in article:
        errors.append("Main table differs from CSV: " + row["model"])
    for key in ("keyword_count_proxy", "state_micro_f1", "report_micro_f1", "disagreement"):
        if row[key] and not 0 <= float(row[key]) <= 1:
            errors.append("Invalid metric range")
if next(x for x in main if x["model"] == "C3-filtered")["keyword_count_proxy"]:
    errors.append("Filtered report score was not independently measured")
for row in neg:
    count, n = int(row["reports_with_any_positive"]), int(row["cases"])
    if n != 15 or not 0 <= count <= n or abs(float(row["any_positive_proxy"]) - count / n) > 0.00051:
        errors.append("Invalid negative-control count: " + row["model"])
    if f"| {row['model']} | {count}/{n} | {row['any_positive_proxy']} |" not in article:
        errors.append("Negative-control table differs from CSV: " + row["model"])
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"PASS: {len(files)} whitelisted text files; links, tables, ranges and sensitive patterns checked.")
