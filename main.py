import base64
import time
import requests
from textwrap import dedent
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def initialize_openai_client():
    """Initialize OpenAI client with ARIA credentials"""
    return OpenAI(
        base_url=os.getenv('ARIA_BASE_URL'),
        api_key=os.getenv('ARIA_API_KEY')
    )

def image_to_base64(image_path):
    """Converts an image to a base64-encoded string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        raise FileNotFoundError("Image file not found. Please check the path.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

def analyze_image_with_aria(client, base64_image):
    """Analyze image using ARIA API and get scene descriptions"""
    response = client.chat.completions.create(
        model="aria",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    {"type": "text", "text": dedent("""\
                    <image>\nThis is an image of a place. Give three scenes and descriptions to bring it to life. Format:

                    Scene <number>: <engaging description>

                    Return 3 scenes in that format only.
                    """)}
                ]
            }
        ],
        stream=False,
        temperature=0.6,
        max_tokens=1024,
        top_p=1,
        stop=["<|im_end|>"]
    )
    return response.choices[0].message.content

def generate_video(scenes):
    """Generate video based on scene descriptions"""
    url = f"{os.getenv('ARIA_BASE_URL')}/generateVideoSyn"
    headers = {
        "Authorization": f"Bearer {os.getenv('ALLEGRO_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "refined_prompt": scenes,
        "num_step": 100,
        "cfg_scale": 7.5,
        "user_prompt": scenes,
        "rand_seed": 12345
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json().get('data')

def query_video_status(request_id, wait_time=120):
    """Query video generation status and return video link"""
    time.sleep(wait_time)

    url = f"{os.getenv('ARIA_BASE_URL')}/videoQuery"
    headers = {
        "Authorization": f"Bearer {os.getenv('ALLEGRO_API_KEY')}",
    }
    params = {"requestId": request_id}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get('data')

def process_travel_image(image_path, wait_time=120):
    """Main function to process travel image and generate video"""
    try:
        # Initialize OpenAI client
        client = initialize_openai_client()

        # Convert image to base64
        base64_image = image_to_base64(image_path)

        # Analyze image with ARIA
        scenes = analyze_image_with_aria(client, base64_image)
        print("Scene descriptions generated:")
        print(scenes)

        # Generate video
        request_id = generate_video(scenes)
        print(f"Video generation started with request ID: {request_id}")

        # Query video status
        video_link = query_video_status(request_id, wait_time)
        print(f"Video link: {video_link}")

        return video_link

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    image_path = "/home/bilal/projects/aria_and_alegro/download.png"
    video_link = process_travel_image(image_path)