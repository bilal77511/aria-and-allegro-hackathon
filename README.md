# Poetry Video Generator 🎥

An AI-powered application that transforms poetry into captivating multimedia experiences. This project seamlessly integrates ARIA AI for poetry composition, OpenAI for natural text-to-speech conversion, and Allegro AI for dynamic video generation.

## ✨ Features

- 📝 Generate unique poems across diverse styles and languages
- 🗣️ Convert text to lifelike speech using advanced AI
- 🎬 Create stunning AI-generated background visuals
- 🎨 Apply professional video effects and audio synchronization
- 🌐 Intuitive web interface for seamless creation

## 🚀 Requirements

- Python 3.8+
- OpenAI API key
- ARIA API key
- Allegro API key

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/poetry-video-generator.git
cd poetry-video-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
ARIA_API_KEY=your_aria_api_key
ARIA_BASE_URL=https://api.rhymes.ai/v1
ALLEGRO_API_KEY=your_allegro_api_key
```

## 📱 Usage

### Web Interface
Launch the Streamlit web application:
```bash
streamlit run app.py
```

### Command Line
Run via command line:
```bash
python main.py
```

## 🏗️ Project Structure

```
poetry-video-generator/
├── aria.py           # Poetry generation engine
├── tts.py            # Text-to-speech conversion
├── allegro.py        # Video generation system
├── video_downloader.py # Video download manager
├── video_editor.py   # Video editing suite
├── app.py           # Web interface
└── main.py          # CLI application
```

## 🔧 Core Components

- **Poetry Generation**: Leverages ARIA AI for creating unique verses
- **Speech Synthesis**: Uses OpenAI's advanced TTS models
- **Video Creation**: Employs Allegro AI for visual generation
- **Video Processing**: Custom editing pipeline for final output

## 🌟 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Developer**: Your Name
- 📧 Email: your.email@example.com
- 💻 GitHub: [@yourusername](https://github.com/yourusername)
- 🌐 Project: [poetry-video-generator](https://github.com/yourusername/poetry-video-generator)
