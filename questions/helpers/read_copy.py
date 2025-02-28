import cv2
import numpy as np
import pytesseract
from PIL import Image
import fitz
from realesrgan import RealESRGAN

def enhance_resolution(image):
    """Enhances image resolution using RealESRGAN."""
    model = RealESRGAN(None, scale=4)
    model.load_weights('RealESRGAN_x4plus.pth', download=True)

    enhanced_image = model.predict(np.array(image))
    return Image.fromarray(cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB))

def sharpen_image(image):
    """Sharpens the image."""
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(np.array(image), -1, kernel)
    return Image.fromarray(sharpened)

def denoise_image(image):
    """Denoises the image."""
    denoised = cv2.fastNlMeansDenoisingColored(np.array(image), None, 10, 10, 7, 21)
    return Image.fromarray(denoised)

def preprocess_image(image):
    """Preprocesses the image for better OCR results."""
    enhanced = enhance_resolution(image)
    sharpened = sharpen_image(enhanced)
    denoised = denoise_image(sharpened)

    gray = cv2.cvtColor(np.array(denoised), cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    return dilated

def perform_ocr(image, lang='eng'):
    """Performs OCR on the image."""
    try:
        preprocessed = preprocess_image(image)
        pil_img = Image.fromarray(preprocessed)
        text = pytesseract.image_to_string(pil_img, lang=lang)
        return text.strip()
    except pytesseract.TesseractError as e:
        return f"Tesseract Error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def ocr_pdf(pdf_path, lang='eng'):
    """Performs OCR on a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += perform_ocr(img, lang) + "\n"
        return text
    except FileNotFoundError:
        return "PDF not found."
    except Exception as e:
        return f"PDF Error: {e}"
