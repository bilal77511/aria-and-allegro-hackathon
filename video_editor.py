import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from pathlib import Path

class VideoEditor:
    def __init__(self):
        """Initialize the Video Editor"""
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(exist_ok=True)

    def reverse_video(self, video_path, output_path):
        """
        Reverse a video
        
        Args:
            video_path (str): Path to input video
            output_path (str): Path for reversed video
        """
        try:
            # Open the original video
            cap = cv2.VideoCapture(video_path)
            
            # Get properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Read frames into a list
            frames = []
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            
            cap.release()

            # Write reversed frames
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            for frame in reversed(frames):
                out.write(frame)

            out.release()
            
        except Exception as e:
            raise Exception(f"Failed to reverse video: {str(e)}")

    def create_video_with_audio(self, video_path, audio_path, output_path=None):
        """
        Create a video with audio, using reversed video effect
        
        Args:
            video_path (str): Path to input video
            audio_path (str): Path to audio file
            output_path (str, optional): Path for output video
        
        Returns:
            str: Path to the created video
        """
        try:
            if output_path is None:
                output_path = str(self.output_dir / "final_video.mp4")
            
            # Create reversed video
            reversed_path = str(self.output_dir / "temp_reversed.mp4")
            self.reverse_video(video_path, reversed_path)
            
            # Load videos and audio
            original_video = VideoFileClip(video_path)
            reversed_video = VideoFileClip(reversed_path)
            audio = AudioFileClip(audio_path)
            
            # Combine videos
            combined_video = concatenate_videoclips([original_video, reversed_video])
            
            # Create final video matching audio duration
            clips = []
            current_duration = 0
            while current_duration < audio.duration:
                clips.append(combined_video)
                current_duration += combined_video.duration

            final_video = concatenate_videoclips(clips).set_duration(audio.duration)
            final_video = final_video.set_audio(audio)

            # Export
            print("Exporting final video...")
            final_video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )
            
            # Cleanup
            original_video.close()
            reversed_video.close()
            audio.close()
            final_video.close()
            if Path(reversed_path).exists():
                Path(reversed_path).unlink()
                
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to create video with audio: {str(e)}")
