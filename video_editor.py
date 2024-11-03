from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from pathlib import Path
import tempfile

class VideoEditor:
    def __init__(self):
        """Initialize the Video Editor using temporary directory"""
        self.output_dir = Path(tempfile.gettempdir())  # Use system temp directory

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
            
            # Load original video
            original_video = VideoFileClip(video_path)
            
            # Create reversed version using moviepy instead of OpenCV
            reversed_video = original_video.copy()
            reversed_video = reversed_video.fx(vfx.time_mirror)
            
            # Load audio
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
                
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to create video with audio: {str(e)}")
