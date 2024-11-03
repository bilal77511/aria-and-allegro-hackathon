from aria import AriaTextGenerator
from tts import TextToSpeech
from allegro import VideoGenerator
from video_downloader import VideoDownloader
from tqdm import tqdm

def main():
    # Initialize all components
    aria_generator = AriaTextGenerator()
    tts_generator = TextToSpeech()
    video_generator = VideoGenerator()
    video_downloader = VideoDownloader()
    
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
        
        # Generate video
        print("\nGenerating video...")
        prompt = "A serene natural scene with gentle movements, perfect for poetry background"
        request_id, video_url = video_generator.create_video(
            prompt=prompt,
            wait_for_completion=True
        )
        
        if video_url:
            print(f"Video generated successfully!")
            print(f"Video URL: {video_url}")
            
            # Download the video
            print("\nDownloading video...")
            video_path = video_downloader.download_video(
                url=video_url,
                filename="poetry_background.mp4"
            )
            
            # Get and display video info
            video_info = video_downloader.get_video_info(video_path)
            print("\nVideo Information:")
            print(f"Location: {video_info['path']}")
            print(f"Size: {video_info['size_mb']:.2f} MB")
            
        else:
            print(f"Video generation started. Request ID: {request_id}")
            print("Check status later using the request ID")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()