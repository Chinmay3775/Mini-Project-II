<div align="center">
  <img src="https://i.imgur.com/NZkRxpg.png" alt="Project Banner" width="850"/>
  <h1>AI-Powered Vocabulary Learning Tool</h1>
  <p><i>Enhance vocabulary through interactive image-recognition flashcards</i></p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white"/>
  <img src="https://img.shields.io/badge/gTTS-FF9800?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
</p>

<div align="center">
  <h3>📋 Contents</h3>
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#future-improvements">Future Improvements</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a> •
  <a href="#author">Author</a>
</div>

<div align="center">
  <img src="https://i.imgur.com/XrEAaoj.png" alt="Application Screenshots" width="750"/>
</div>

<h2 id="overview">🧠 Overview</h2>

**Mini-Project-II** is an AI-powered educational tool designed to enhance vocabulary learning through interactive flashcards. By leveraging image recognition and text-to-speech technologies, the application provides an engaging platform for users to associate words with images and hear their pronunciations, facilitating a multisensory learning experience.

<div align="center">
  <img src="https://i.imgur.com/i5c0aGn.png" alt="How It Works" width="650"/>
</div>

<h2 id="features">🚀 Features</h2>

<table>
  <tr>
    <td width="50%">
      <h3 align="center">📷 Image Recognition</h3>
      <div align="center">
        <img src="https://i.imgur.com/TrHQpLg.png" alt="Image Recognition" width="300"/>
      </div>
      <p align="center">Upload images to identify and extract relevant vocabulary</p>
    </td>
    <td width="50%">
      <h3 align="center">🔊 Text-to-Speech</h3>
      <div align="center">
        <img src="https://i.imgur.com/WS2uDgJ.png" alt="Text to Speech" width="300"/>
      </div>
      <p align="center">Hear pronunciations using Google TTS technology</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3 align="center">🃏 Interactive Flashcards</h3>
      <div align="center">
        <img src="https://i.imgur.com/4nNFn1e.png" alt="Flashcards" width="300"/>
      </div>
      <p align="center">Learn vocabulary using visual + audio learning cards</p>
    </td>
    <td width="50%">
      <h3 align="center">💡 User-Friendly Interface</h3>
      <div align="center">
        <img src="https://i.imgur.com/yl75GKw.png" alt="Interface" width="300"/>
      </div>
      <p align="center">Clean and intuitive web design built with Flask</p>
    </td>
  </tr>
</table>

<h2 id="demo">📱 Demo</h2>

<div align="center">
  <img src="https://i.imgur.com/m5vTZQm.gif" alt="Application Demo" width="650"/>
  <p><i>Demo of the application workflow: Upload Image → Generate Flashcard → Learn Vocabulary</i></p>
</div>

<h2 id="project-structure">📁 Project Structure</h2>

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

<div align="center">
  <img src="https://i.imgur.com/dA51BhC.png" alt="Architecture Diagram" width="650"/>
  <p><i>System Architecture Diagram</i></p>
</div>

<h2 id="installation">⚙️ Installation & Setup</h2>

<div align="center">
  <img src="https://i.imgur.com/Npsfdm9.png" alt="Installation Steps" width="650"/>
</div>

1. **Clone the Repository**
```bash
git clone https://github.com/Chinmay3775/Mini-Project-II.git
cd Mini-Project-II
```

2. **(Optional) Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # or on Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the App**
```bash
python app.py
```

5. **Access the App**
Open your browser and go to `http://localhost:5000`

<h2 id="usage">🧪 Usage</h2>

<div align="center">
  <table>
    <tr>
      <td><img src="https://i.imgur.com/l37NSXT.png" alt="Step 1" width="200"/></td>
      <td><img src="https://i.imgur.com/Yk7yQ0r.png" alt="Step 2" width="200"/></td>
      <td><img src="https://i.imgur.com/0B4yigL.png" alt="Step 3" width="200"/></td>
    </tr>
    <tr>
      <td align="center">1. Upload an image</td>
      <td align="center">2. AI identifies the object</td>
      <td align="center">3. Learn with audio pronunciation</td>
    </tr>
  </table>
</div>

<h2 id="future-improvements">🌱 Future Improvements</h2>

<div align="center">
  <img src="https://i.imgur.com/QVHtlzc.png" alt="Future Roadmap" width="650"/>
</div>

<table>
  <tr>
    <td><img src="https://img.shields.io/badge/-Multilingual-9C27B0?style=for-the-badge" alt="Multilingual"/></td>
    <td>Support for multiple languages to enhance global vocabulary learning</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/-Performance_Tracking-FFC107?style=for-the-badge" alt="Performance Tracking"/></td>
    <td>Track user progress and suggest personalized learning paths</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/-Mobile_Integration-4CAF50?style=for-the-badge" alt="Mobile Integration"/></td>
    <td>Develop mobile app versions for iOS and Android platforms</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/-Expanded_Dataset-FF5722?style=for-the-badge" alt="Expanded Dataset"/></td>
    <td>Enlarge the vocabulary dataset for better image recognition</td>
  </tr>
</table>

<h2 id="contributing">🤝 Contributing</h2>

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

<h2 id="license">📄 License</h2>

This project is licensed under the [MIT License](LICENSE).

<h2 id="author">👤 Author</h2>

<div align="center">
  <img src="https://i.imgur.com/SZClohf.png" alt="Author" width="150" style="border-radius:50%"/>
  <h3>Chinmay Keripale</h3>
  <p>Software Engineer & AI Enthusiast</p>
  <a href="https://github.com/Chinmay3775">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</div>

---

<div align="center">
  <small>© 2023 Chinmay Keripale. All rights reserved.</small>
</div>
