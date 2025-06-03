import cv2
import pytesseract
import numpy as np
from PIL import Image
from skimage.filters import threshold_local
from scipy.ndimage import deskew
import imutils
import re
# Optional libraries for advanced features
try:
    import easyocr
except ImportError:
    print("Warning: easyocr not installed. Handwritten text extraction will be limited.")
try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    trocr_processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
except ImportError:
    print("Warning: transformers not installed. TrOCR functionality will be limited.")
try:
    from langdetect import detect
except ImportError:
    print("Warning: langdetect not installed. Automatic language detection will be limited.")
try:
    from textblob import TextBlob
except ImportError:
    print("Warning: textblob not installed. Spell correction will be limited.")
try:
    import layoutparser as lp
except ImportError:
    print("Warning: layoutparser not installed. Region segmentation will be limited.")

def enhance_contrast_clahe(gray_image):
    """Applies Contrast Limited Adaptive Histogram Equalization (CLAHE)."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray_image)

def apply_morphological_operations(binary_image, operation='dilate', kernel_size=(5, 5), iterations=1):
    """Applies morphological operations (dilation or erosion)."""
    kernel = np.ones(kernel_size, np.uint8)
    if operation == 'dilate':
        return cv2.dilate(binary_image, kernel, iterations=iterations)
    elif operation == 'erode':
        return cv2.erode(binary_image, kernel, iterations=iterations)
    return binary_image

def deskew_image(image):
    """Deskews an image to correct for slight rotations."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def remove_shadows(image):
    """Attempts to remove shadows from an image."""
    rgb_planes = cv2.split(image)
    result_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        result_planes.append(norm_img)
    return cv2.merge(result_planes)

def preprocess_image_advanced(image_path, deskew=False, enhance_contrast=False, morphological_op=None):
    """Load and preprocess the image for OCR with advanced techniques."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Error: Unable to load image {image_path}")

        if deskew:
            img = deskew_image(img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if enhance_contrast:
            gray = enhance_contrast_clahe(gray)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        processed = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        if morphological_op:
            processed = apply_morphological_operations(processed, operation=morphological_op)

        return processed

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def extract_text_advanced(image_path, handwritten=False, languages='eng', segment_regions=False):
    """Extract text with OCR, supporting advanced features."""
    if handwritten:
        try:
            reader = easyocr.Reader([languages])
            result = reader.readtext(image_path)
            text = " ".join([item[1] for item in result])
            return text.strip()
        except NameError:
            print("Error: easyocr not installed. Cannot perform handwritten text extraction.")
            return ""
        except Exception as e:
            print(f"Error during handwritten OCR: {e}")
            return ""
    else:
        processed_img = preprocess_image_advanced(image_path, deskew=True, enhance_contrast=True, morphological_op='erode')
        if processed_img is None:
            return ""
        try:
            text = pytesseract.image_to_string(processed_img, config=f"--psm 6 --oem 3 -l {languages}", output_type=pytesseract.Output.STRING)
            return text.strip()
        except Exception as e:
            print(f"Error during OCR: {e}")
            return ""

def extract_text_trocr(image_path):
    """Extract text from handwritten images using TrOCR."""
    try:
        image = Image.open(image_path).convert("RGB")
        pixel_values = trocr_processor(images=image, return_tensors="pt").pixel_values
        generated_ids = trocr_model.generate(pixel_values)
        text = trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return text.strip()
    except NameError:
        print("Error: transformers not installed. Cannot use TrOCR.")
        return ""
    except Exception as e:
        print(f"Error during TrOCR extraction: {e}")
        return ""

def detect_language(text):
    """Detect the language of the given text."""
    try:
        return detect(text)
    except NameError:
        print("Warning: langdetect not installed. Language detection not available.")
        return None
    except Exception as e:
        print(f"Error during language detection: {e}")
        return None

def extract_text_multilingual(image_path):
    """Extract text, attempting to handle multiple languages."""
    processed_img = preprocess_image_advanced(image_path, deskew=True, enhance_contrast=True, morphological_op='erode')
    if processed_img is None:
        return ""
    try:
        text = pytesseract.image_to_string(processed_img, config="--psm 6 --oem 3", output_type=pytesseract.Output.STRING)
        detected_lang = detect_language(text)
        if detected_lang:
            print(f"Detected language: {detected_lang}")
            text_with_lang = pytesseract.image_to_string(processed_img, config=f"--psm 6 --oem 3 -l {detected_lang}")
            return text_with_lang.strip()
        return text.strip()
    except Exception as e:
        print(f"Error during multilingual OCR: {e}")
        return ""

def segment_and_extract(image_path):
    """Segments the image into regions and extracts text from each."""
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Error: Unable to load image {image_path}")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        model = lp.models.TesseractOcrLayoutModel(config_path="lp_config.yaml", model_path="tesseract", extra_config=["--oem", "3", "--psm", "6"]) # You might need to configure the path
        layout = model.detect(image)

        extracted_regions = {}
        for i, block in enumerate(layout):
            x_1, y_1, x_2, y_2 = block.coordinates
            roi = gray[int(y_1):int(y_2), int(x_1):int(x_2)]
            _, binary_roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            text = pytesseract.image_to_string(binary_roi, config="--psm 6 --oem 3")
            extracted_regions[f"region_{i}"] = text.strip()
        return extracted_regions
    except NameError:
        print("Warning: layoutparser not installed. Region segmentation not available.")
        return {}
    except Exception as e:
        print(f"Error during region segmentation and extraction: {e}")
        return {}

def correct_spelling(text):
    """Corrects spelling mistakes in the given text."""
    try:
        blob = TextBlob(text)
        return str(blob.correct())
    except NameError:
        print("Warning: textblob not installed. Spell correction not available.")
        return text
    except Exception as e:
        print(f"Error during spell correction: {e}")
        return text

def remove_unwanted_characters(text, pattern=r'[^a-zA-Z0-9\s.,?!;:\'"()\[\]{}]'):
    """Removes unwanted characters from the text using regex."""
    return re.sub(pattern, '', text)

def extract_text_with_postprocessing(image_path):
    """Extracts text and applies spell correction and unwanted character removal."""
    extracted_text = extract_text_advanced(image_path)
    corrected_text = correct_spelling(extracted_text)
    cleaned_text = remove_unwanted_characters(corrected_text)
    return cleaned_text

def get_confidence_and_highlight(image_path):
    """Extracts text with confidence scores and highlights low confidence words."""
    processed_img = preprocess_image_advanced(image_path, deskew=True, enhance_contrast=True, morphological_op='erode')
    if processed_img is None:
        return None, None
    try:
        data = pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT)
        n_boxes = len(data['text'])
        confs = []
        text_with_confidence = []
        img_with_highlight = cv2.imread(image_path)
        if img_with_highlight is None:
            return None, None

        for i in range(n_boxes):
            if int(data['conf'][i]) > 0:
                confs.append(int(data['conf'][i]))
                text_with_confidence.append((data['text'][i], int(data['conf'][i])))
                if int(data['conf'][i]) < 60: # Example threshold for low confidence
                    x, y, w, h = int(data['left'][i]), int(data['top'][i]), int(data['width'][i]), int(data['height'][i])
                    cv2.rectangle(img_with_highlight, (x, y), (x + w, y + h), (0, 0, 255), 2) # Red for low confidence

        return text_with_confidence, img_with_highlight
    except Exception as e:
        print(f"Error during confidence analysis: {e}")
        return None, None

def add_watermark(image_path, watermark_text="CONFIDENTIAL"):
    """Adds a watermark to the image."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to load image {image_path} for watermarking.")
        return None
    height, width, _ = img.shape
    text_size = cv2.getTextSize(watermark_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = (width - text_size[0]) // 2
    text_y = height - 50
    cv2.putText(img, watermark_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    return img

# Example Usage:
if __name__ == "__main__":
    image_file = "sample.png" # Replace with your image path

    # Basic OCR
    basic_text = extract_text(image_file)
    print("Basic OCR Output:\n", basic_text)
    print("-" * 30)

    # Advanced OCR with preprocessing
    advanced_text = extract_text_advanced(image_file)
    print("Advanced OCR Output:\n", advanced_text)
    print("-" * 30)

    # Handwritten Text Extraction (if easyocr is installed)
    handwritten_text_easyocr = extract_text_advanced(image_file, handwritten=True)
    print("Handwritten Text (EasyOCR):\n", handwritten_text_easyocr)
    print("-" * 30)

    # Handwritten Text Extraction (if transformers is installed)
    handwritten_text_trocr = extract_text_trocr(image_file)
    print("Handwritten Text (TrOCR):\n", handwritten_text_trocr)
    print("-" * 30)

    # Multilingual OCR
    multilingual_text = extract_text_multilingual(image_file)
    print("Multilingual OCR Output:\n", multilingual_text)
    print("-" * 30)

    # Region Segmentation and Extraction (if layoutparser is installed)
    segmented_text = segment_and_extract(image_file)
    print("Segmented Text:\n", segmented_text)
    print("-" * 30)

    # OCR with Post-processing (Spell Correction and Cleanup)
    postprocessed_text = extract_text_with_postprocessing(image_file)
    print("OCR with Post-processing:\n", postprocessed_text)
    print("-" * 30)

    # Confidence Score and Highlighting
    confidence_data, highlighted_image = get_confidence_and_highlight(image_file)
    if confidence_data:
        print("Text with Confidence Scores:\n", confidence_data)
        if highlighted_image is not None:
            cv2.imwrite("highlighted_image.png", highlighted_image)
            print("Low confidence words highlighted in 'highlighted_image.png'")
    print("-" * 30)

    # Adding Watermark
    watermarked_image = add_watermark(image_file)
    if watermarked_image is not None:
        cv2.imwrite("watermarked_image.png", watermarked_image)
        print("Image watermarked and saved as 'watermarked_image.png'")