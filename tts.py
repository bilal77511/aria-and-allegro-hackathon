from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

class TextToSpeech:
    def __init__(self):
        """Initialize the TTS generator with OpenAI client"""
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(exist_ok=True)  # Create output directory if it doesn't exist

    def generate_speech(self, text, filename="speech.mp3", voice="onyx"):
        """
        Generate speech from text
        
        Args:
            text (str): Text to convert to speech
            filename (str): Output filename (default: speech.mp3)
            voice (str): Voice to use (default: onyx)
            
        Returns:
            Path: Path to the generated audio file
        """
        try:
            speech_file_path = self.output_dir / filename
            
            # Make the API call to generate the TTS audio
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )

            # Write the binary audio content to the file
            with open(speech_file_path, "wb") as f:
                f.write(response.content)
            
            return speech_file_path

        except Exception as e:
            raise Exception(f"Failed to generate speech: {str(e)}")