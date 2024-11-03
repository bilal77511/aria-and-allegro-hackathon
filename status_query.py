import requests
from config import Config

token = Config.ALLEGRO_API_KEY

def query_video_status():

    request_id = input("Please enter the request ID: ")

    url = "https://api.rhymes.ai/v1/videoQuery"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    params = {
        "requestId": request_id
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"


response_data = query_video_status()
print(response_data)