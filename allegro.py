import requests
import time
from pathlib import Path
from dotenv import load_dotenv
import os

class VideoGenerator:
    def __init__(self):
        """Initialize the Video Generator with Allegro credentials"""
        load_dotenv()
        self.base_url = "https://api.rhymes.ai/v1"
        self.api_key = os.getenv('ALLEGRO_API_KEY')
        
    def generate_video(self, prompt, num_steps=100, cfg_scale=7.5, seed=100000):
        """
        Generate a video using Allegro API
        
        Args:
            prompt (str): Description of the video to generate
            num_steps (int): Number of generation steps
            cfg_scale (float): Configuration scale
            seed (int): Random seed for generation
            
        Returns:
            str: Request ID for the video generation task
        """
        url = f"{self.base_url}/generateVideoSyn"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "refined_prompt": prompt,
            "num_step": num_steps,
            "cfg_scale": cfg_scale,
            "user_prompt": prompt,
            "rand_seed": seed
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json().get('data')  # Returns the request ID
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to generate video: {str(e)}")

    def query_video_status(self, request_id, max_retries=10, wait_time=30):
        """
        Query the status of a video generation task
        
        Args:
            request_id (str): The request ID from generate_video
            max_retries (int): Maximum number of retry attempts
            wait_time (int): Time to wait between retries in seconds
            
        Returns:
            str: URL of the generated video
        """
        url = f"{self.base_url}/videoQuery"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        params = {
            "requestId": request_id
        }

        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                video_url = data.get('data')
                if video_url and video_url.strip():
                    return video_url
                
                print(f"Attempt {attempt + 1}/{max_retries}: Video still processing, waiting {wait_time} seconds...")
                time.sleep(wait_time)
                
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                continue
        
        raise Exception("Failed to get video URL after maximum retries")

    def create_video(self, prompt, wait_for_completion=True):
        """
        Convenience method to generate and optionally wait for video completion
        
        Args:
            prompt (str): Description of the video to generate
            wait_for_completion (bool): Whether to wait for the video to complete
            
        Returns:
            tuple: (request_id, video_url if wait_for_completion is True)
        """
        try:
            # Generate the video
            request_id = self.generate_video(prompt)
            print(f"Video generation started with request ID: {request_id}")
            
            if wait_for_completion:
                # Wait for initial processing
                print("Waiting 2 minutes for initial processing...")
                time.sleep(120)
                
                # Query for video URL
                video_url = self.query_video_status(request_id)
                return request_id, video_url
            
            return request_id, None
            
        except Exception as e:
            raise Exception(f"Failed to create video: {str(e)}")