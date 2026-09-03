"""Audit a third-party study archive without copying or executing its content."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlparse
from zipfile import ZipFile


URL = re.compile(r"https?://[^\s)>]+")
WEIGHT_ROW = re.compile(r"\|\s*(\d+)\s*\|.*?\|\s*(\d+)%\s*\|\s*(\d+)\s*\|")


def _safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return not path.is_absolute() and ".." not in path.parts


def audit_zip(path: Path) -> dict[str, object]:
    archive_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    with ZipFile(path) as archive:
        names = archive.namelist()
        unsafe = [name for name in names if not _safe_member(name)]
        files = [name for name in names if not name.endswith("/")]
        roots = {PurePosixPath(name).parts[0] for name in files}
        if len(roots) != 1:
            raise ValueError("archive must contain one top-level directory")
        root = next(iter(roots))
        readme_name = f"{root}/README.md"
        if readme_name not in names:
            raise ValueError("archive README missing")
        readme = archive.read(readme_name).decode("utf-8", errors="replace")
        notes = [name for name in files if name.endswith(".md") and name != readme_name]
        counts = Counter(PurePosixPath(name).parts[1] for name in notes)
        source_counts, all_urls = {}, []
        for name in notes:
            text = archive.read(name).decode("utf-8", errors="replace")
            urls = URL.findall(text)
            source_counts[name] = len(urls); all_urls.extend(urls)
        weight_rows = WEIGHT_ROW.findall(readme)
        licenses = [name for name in files if PurePosixPath(name).name.lower().startswith(("license", "copying"))]
        pdfs = [name for name in files if name.lower().endswith(".pdf")]
        pdf_hashes = {name:hashlib.sha256(archive.read(name)).hexdigest() for name in pdfs}
    return {"archive":str(path), "sha256":archive_hash,
            "zip_comment":archive.comment.decode("utf-8", errors="replace"),
            "path_safe":not unsafe, "unsafe_members":unsafe,
            "markdown_topic_notes":len(notes), "domain_note_counts":dict(sorted(counts.items())),
            "notes_with_sources":sum(count > 0 for count in source_counts.values()),
            "notes_without_sources":[name for name, count in source_counts.items() if count == 0],
            "source_url_count":len(all_urls),
            "source_hosts":dict(sorted(Counter(urlparse(url).netloc for url in all_urls).items())),
            "readme_weights":[{"domain":int(domain), "weight":int(weight), "notes":int(count)}
                              for domain, weight, count in weight_rows],
            "readme_weight_total":sum(int(weight) for _, weight, _ in weight_rows),
            "license_files":licenses, "content_reuse_allowed":bool(licenses),
            "pdf_sha256":pdf_hashes,
            "interpretation":["supplemental third-party index; official NVIDIA guide controls",
                              "absence of a license means do not copy prose into this course",
                              "citations are presence checks, not factual validation"]}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python3 -m assessments.third_party_archive INPUT.zip OUTPUT.json")
    report = audit_zip(Path(sys.argv[1]))
    output = Path(sys.argv[2]); output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {output}; notes={report['markdown_topic_notes']}; license={report['content_reuse_allowed']}")
