import sys
from pypdf import PdfReader

def extract_images_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    images_found = 0
    for page_num, page in enumerate(reader.pages):
        for image_num, image in enumerate(page.images):
            images_found += 1
            with open(f"image_page{page_num}_img{image_num}.png", "wb") as f:
                f.write(image.data)
            print(f"Extracted image_page{page_num}_img{image_num}.png")
    if images_found == 0:
        print("No images found in the PDF.")
    else:
        print(f"Total images extracted: {images_found}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_images.py <pdf_path>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    extract_images_from_pdf(pdf_path)