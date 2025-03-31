import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Set Tesseract OCR Path (Windows Users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def show_image(title, img):
    """ Display an image using Matplotlib. """
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis("off")
    plt.show()

def preprocess_image(image_path):
    """ Load & preprocess the image for OCR """
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray.jpg", gray)

    # Apply Otsu's Thresholding (better than Adaptive Thresholding)
    _, processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("thresholded.jpg", processed)

    # Apply median blur to remove noise
    denoised = cv2.medianBlur(processed, 3)
    cv2.imwrite("denoised.jpg", denoised)

    return denoised  # Return denoised image

def extract_text(image_path):
    """ Extract text from the preprocessed image """
    processed_img = preprocess_image(image_path)

    # Run OCR with improved settings
    text = pytesseract.image_to_string(processed_img, config="--psm 6 --oem 3")
    
    print("Raw OCR Output:\n", repr(text))  # Debugging output
    return text.strip()

if __name__ == "__main__":
    image_path = "imageText1.jpg"  # Use your actual image
    extracted_text = extract_text(image_path)

    print("\nExtracted Text:\n", extracted_text)
