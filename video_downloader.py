import requests
from pathlib import Path
import os
from datetime import datetime
from tqdm import tqdm

class VideoDownloader:
    def __init__(self):
        """Initialize the Video Downloader"""
        self.output_dir = Path(__file__).parent / "videos"
        self.output_dir.mkdir(exist_ok=True)  # Create videos directory if it doesn't exist

    def download_video(self, url, filename=None):
        """
        Download video from URL
        
        Args:
            url (str): URL of the video to download
            filename (str, optional): Custom filename for the video
                                    If None, uses timestamp
        
        Returns:
            Path: Path to the downloaded video file
        """
        try:
            # Generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"video_{timestamp}.mp4"
            
            # Ensure filename has .mp4 extension
            if not filename.endswith('.mp4'):
                filename += '.mp4'
            
            # Full path for the video
            video_path = self.output_dir / filename
            
            # Download the video
            print(f"Downloading video from {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Get total file size for progress tracking
            total_size = int(response.headers.get('content-length', 0))
            
            # Write the file with progress tracking
            with open(video_path, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    progress_bar.update(size)
            
            print(f"Video downloaded successfully to: {video_path}")
            return video_path
            
        except Exception as e:
            raise Exception(f"Failed to download video: {str(e)}")

    def get_video_info(self, video_path):
        """
        Get basic information about the downloaded video
        
        Args:
            video_path (Path): Path to the video file
            
        Returns:
            dict: Video information
        """
        try:
            file_size = os.path.getsize(video_path)
            return {
                'path': video_path,
                'size_bytes': file_size,
                'size_mb': file_size / (1024 * 1024),  # Convert to MB
                'filename': video_path.name
            }
        except Exception as e:
            raise Exception(f"Failed to get video info: {str(e)}")