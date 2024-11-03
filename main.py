from aria import AriaTextGenerator
from tts import TextToSpeech
from allegro import VideoGenerator

def main():
    # Initialize the generators
    aria_generator = AriaTextGenerator()
    tts_generator = TextToSpeech()
    video_generator = VideoGenerator()
    
    try:
        # Generate a poem
        poem = aria_generator.generate_poem(
            style="sad heartbroken",
            verses=2,
            language="english"
        )
        print("Generated Poem:")
        print(poem)
        
        # Generate audio from the poem
        print("\nGenerating audio...")
        audio_path = tts_generator.generate_speech(
            text=poem,
            filename="generated_poem.mp3",
            voice="onyx"
        )
        print(f"Audio generated successfully at: {audio_path}")
        
        # Generate a video
        print("\nGenerating video...")
        prompt = "A serene natural scene with gentle movements, perfect for poetry background"
        request_id, video_url = video_generator.create_video(
            prompt=prompt,
            wait_for_completion=True
        )
        
        if video_url:
            print(f"Video generated successfully!")
            print(f"Video URL: {video_url}")
        else:
            print(f"Video generation started. Request ID: {request_id}")
            print("Check status later using the request ID")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()