# 🧠 Mini-Project-II

![Flashcard App Demo](https://github.com/Chinmay3775/Mini-Project-II/assets/your-username/demo.gif)  
*A smart flashcard app using image recognition and text-to-speech.*

---

## 📸 Preview

<img src="https://github.com/Chinmay3775/Mini-Project-II/assets/your-username/screenshot.png" width="600"/>

> Replace the image/GIF links with your own project screenshots or screen recordings to showcase functionality.

---

## 🚀 Features

- 📷 Upload an image to identify the object using AI
- 🗣️ Generate flashcards with pronunciation using Google TTS
- 🧠 Enhance vocabulary with audio + visual learning
- 🎨 Simple web interface with clean styling

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![gTTS](https://img.shields.io/badge/gTTS-FF4088?style=for-the-badge)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)

---

## 📁 Project Structure

```
Mini-Project-II/
├── app.py                  # Flask backend entry point
├── main.py                 # Main logic handler
├── flashcard.py            # Flashcard creation
├── image_processing.py     # Image analysis and recognition
├── text_to_speech.py       # Convert text to audio
├── styles.css              # Web styling
├── templates/
│   └── index.html          # Webpage UI
├── static/
│   └── flashcard.mp3       # TTS output
├── temp_image.png          # Temporary uploaded image
└── README.md               # This file
```

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/Chinmay3775/Mini-Project-II.git
cd Mini-Project-II

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://localhost:5000` in your browser to use the app.

---

## 🎯 Usage

1. Upload an image.
2. The system identifies the object and creates a flashcard.
3. Click the audio button to hear its pronunciation.

---

## 🌱 Future Scope

- 🌍 Multilingual support
- 📊 User progress tracking
- 📱 Mobile-responsive design

---

## 🤝 Contributing

We welcome contributions!  
Please fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Chinmay Keripale**  
📌 GitHub: [@Chinmay3775](https://github.com/Chinmay3775)

---

