import os
import cv2
import easyocr
from pdf2image import convert_from_path

# Initialize EasyOCR only once
reader = easyocr.Reader(["en"], gpu=False)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def pdf_to_image(pdf_path):
    """
    Convert the first page of a PDF to PNG.
    Returns the PNG image path.
    """

    pages = convert_from_path(pdf_path)

    if len(pages) == 0:
        raise Exception("No pages found in PDF.")

    image_path = os.path.join(
        UPLOAD_FOLDER,
        "temp_page.png"
    )

    pages[0].save(image_path, "PNG")

    return image_path


def preprocess(image_path):
    """
    Preprocess image for better OCR.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise Exception(f"Cannot open image: {image_path}")

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    processed_path = os.path.join(
        UPLOAD_FOLDER,
        "preprocessed.png"
    )

    cv2.imwrite(
        processed_path,
        thresh
    )

    return processed_path


def clean_text(text):
    """
    Remove unnecessary blank lines.
    """

    cleaned = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            cleaned.append(line)

    return "\n".join(cleaned)


def extract_text(file_path):
    """
    Returns:
        OCR Text
        Image path for LLaVA
    """

    extension = os.path.splitext(file_path)[1].lower()

    # -------------------------
    # PDF -> Image
    # -------------------------

    if extension == ".pdf":
        image_path = pdf_to_image(file_path)
    else:
        image_path = file_path

    processed = preprocess(image_path)

    result = reader.readtext(
        processed,
        detail=0,
        paragraph=False
    )

    text = "\n".join(result)

    cleaned_text = clean_text(text)

    # Return BOTH OCR text and image path
    return cleaned_text, image_path