# -*- coding: utf-8 -*-
import argparse
import json
import re
from pathlib import Path
from typing import List

from pypdf import PdfReader

DEFAULT_DOWNLOADS = Path(r"C:\Users\SANG DUCK\Downloads")
DEFAULT_PATTERN = "TalkFile*.pdf"
PRICE_PATTERN = re.compile(r"(?:Rp\.?|IDR)?\s*([0-9]{1,3}(?:[.,][0-9]{3})*|[0-9]+)")


def normalize_line(line: str) -> str:
    if not line:
        return ""
    return " ".join(line.strip().split())


def parse_price(text: str) -> int | None:
    match = PRICE_PATTERN.search(text)
    if not match:
        return None
    raw = match.group(1)
    digits = re.sub(r"[^0-9]", "", raw)
    if not digits:
        return None
    return int(digits)


def split_name_price(line: str) -> tuple[str | None, int | None]:
    price = parse_price(line)
    if price is None:
        return None, None

    cleaned = PRICE_PATTERN.sub("", line).strip()
    if cleaned:
        return cleaned, price
    return None, price


def parse_menu_lines(lines: List[str]) -> List[dict]:
    items = []
    pending_name = None

    for raw in lines:
        line = normalize_line(raw)
        if not line:
            continue

        name, price = split_name_price(line)
        if price is None:
            pending_name = line
            continue

        if name is None and pending_name:
            name = pending_name
            pending_name = None

        if name is None:
            name = line.replace(str(price), "").strip()
            if not name:
                name = "상품"

        items.append({
            "name": name,
            "price": price,
            "desc": "PDF에서 추출된 메뉴 항목",
            "raw": raw,
        })

    return items


def extract_text_from_pdf(path: Path, max_pages: int = 20) -> str:
    reader = PdfReader(path)
    text_parts = []
    for page_index, page in enumerate(reader.pages[:max_pages]):
        page_text = page.extract_text() or ""
        if page_text.strip():
            text_parts.append(page_text)
    return "\n".join(text_parts)


def find_pdf_files(pattern: str | None, downloads: Path) -> List[Path]:
    if pattern:
        found = sorted(downloads.glob(pattern))
        if found:
            return found

    found = sorted(downloads.glob(DEFAULT_PATTERN))
    if found:
        return found

    return sorted(downloads.glob("*.pdf"))


def format_js_items(items: List[dict], start_id: int = 1000) -> str:
    lines = []
    for index, item in enumerate(items, start=start_id):
        name = item["name"].replace("'", "\\'")
        desc = item["desc"].replace("'", "\\'")
        lines.append(
            f"{{ id: {index}, name: '{name}', price: {item['price']}, desc: '{desc}', img: IMG.KOREAN_BBQ }}"
        )
    return ",\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse menu items from PDF files and export structured output.")
    parser.add_argument("--pattern", default=None, help="PDF filename glob pattern to search in Downloads.")
    parser.add_argument("--file", default=None, help="Specific PDF file to parse.")
    parser.add_argument("--output", default="parsed_menu.json", help="JSON output file path.")
    args = parser.parse_args()

    downloads = DEFAULT_DOWNLOADS
    if args.file:
        path = Path(args.file)
        if path.exists() and path.suffix.lower() == ".pdf":
            pdf_files = [path]
        else:
            print(f"PDF file not found: {args.file}")
            return
    else:
        pdf_files = find_pdf_files(args.pattern, downloads)

    if not pdf_files:
        print(f"No PDF files found in {downloads}. Put your PDF in the Downloads folder or pass --file.")
        return

    print("Found PDF files:")
    for path in pdf_files:
        print(f"  {path.name}")

    all_items = []
    for pdf_file in pdf_files:
        print(f"\n=== Parsing {pdf_file.name} ===")
        text = extract_text_from_pdf(pdf_file, max_pages=20)
        if not text.strip():
            print("  No text could be extracted from this PDF.")
            continue

        raw_lines = [line for line in text.splitlines() if line.strip()]
        items = parse_menu_lines(raw_lines)
        print(f"  Parsed {len(items)} candidate items.")
        for item in items[:20]:
            print(f"    - {item['name']} : Rp {item['price']:,}")
        all_items.extend(items)

    output_path = Path(args.output)
    output_path.write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved parsed menu to {output_path}")
    print("\nJavaScript-ready item entries:")
    print(format_js_items(all_items, start_id=1000))


if __name__ == "__main__":
    main()
