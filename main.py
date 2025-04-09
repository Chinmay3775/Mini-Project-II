from image_processing import extract_text
from text_to_speech import text_to_speech

if __name__ == "__main__":
    image_path = "D:\\Mini-Project II\\Mini-Project-II\\Image_Recognition\\imageText1.png"
    extracted_text = extract_text(image_path)

    print("\nExtracted Flashcard Text:\n", extracted_text)
    text_to_speech(extracted_text)
