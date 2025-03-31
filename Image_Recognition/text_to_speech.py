from gtts import gTTS
import os

def text_to_speech(text, filename="flashcard.mp3"):
    """ Convert extracted text to speech and save as an audio file """
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    print(f"Flashcard audio saved as {filename}")
    os.system(f"start {filename}")  # For Windows, use "start"; for Mac/Linux, use "afplay" or "mpg321"

if __name__ == "__main__":
    sample_text = "Machine learning is a method of data analysis that automates analytical model building."
    text_to_speech(sample_text)
