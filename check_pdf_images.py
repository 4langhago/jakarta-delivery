import argparse
import io
from pathlib import Path
from pypdf import PdfReader


def check_pdf_images(pdf_path: str, out_dir: str = '.') -> int:
    p = Path(pdf_path)
    print(f"Checking PDF: {p}")
    print(f"PDF exists: {p.exists()}")
    if not p.exists():
        return 0

    reader = PdfReader(str(p))
    print(f"Total pages: {len(reader.pages)}")
    images_found = 0

    for page_num, page in enumerate(reader.pages, 1):
        images = getattr(page, 'images', None)
        if not images:
            continue
        for idx, img in enumerate(images, 1):
            images_found += 1
            name = f"page{page_num}_{idx}.png"
            try:
                data = img.data
                with open(Path(out_dir) / name, 'wb') as f:
                    f.write(data)
                print(f"Image found on page {page_num}: saved as {name}")
            except Exception as e:
                print(f"  -> Error saving {name}: {e}")

    print(f"\nTotal images found: {images_found}")
    return images_found


def main():
    parser = argparse.ArgumentParser(description='Check and dump images from PDF')
    parser.add_argument('pdf', help='Path to PDF')
    parser.add_argument('--out', default='.', help='Output directory for extracted images')
    args = parser.parse_args()
    check_pdf_images(args.pdf, args.out)


if __name__ == '__main__':
    main()
