import argparse
import io
from pathlib import Path
from pypdf import PdfReader
from PIL import Image


def extract_all_images(pdf_path: str, output_dir: str = "menu_images") -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(pdf_path)
    image_data = {}
    total = 0

    for page_num, page in enumerate(reader.pages, 1):
        image_data[page_num] = []
        images = getattr(page, "images", None)
        if not images:
            continue

        for idx, img in enumerate(images):
            try:
                data = img.data
                bio = io.BytesIO(data)
                pil = Image.open(bio).convert("RGBA")
                ext = pil.format.lower() if pil.format else "png"
                filename = f"page{page_num:02d}_img{idx:02d}.{ext if ext in ('png','jpeg','jpg') else 'png'}"
                filepath = out / filename
                pil.save(filepath)
                image_data[page_num].append({
                    "file": filename,
                    "size": pil.size
                })
                total += 1
                print(f"Saved: {filename} ({pil.size[0]}x{pil.size[1]})")
            except Exception as e:
                print(f"Error extracting image on page {page_num} idx {idx}: {e}")

    print(f"Total images extracted: {total}")
    return image_data


def main():
    parser = argparse.ArgumentParser(description="Extract images from a PDF into a folder.")
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("--out", default="menu_images", help="Output directory")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        return

    print(f"Extracting images from: {pdf_path}\n")
    image_data = extract_all_images(str(pdf_path), args.out)
    pages_with = [p for p in image_data if image_data[p]]
    print(f"\nTotal pages with images: {len(pages_with)}")
    for page_num in sorted(image_data.keys()):
        if image_data[page_num]:
            print(f"Page {page_num}: {len(image_data[page_num])} images")


if __name__ == "__main__":
    main()
