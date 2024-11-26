import requests
from pprint import pprint
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sends image to Pl@ntnet API for possible identification'

    def handle(self, *args, **kwargs):

        if not settings.PLANTNET_ENABLED:
            print("Connection to PlantNet not enabled")
            return

        API_KEY = settings.PLANTNET_API_KEY # Replace with your API_KEY
        PROJECT = "all"  # Options: "all", "weurope", "canada"
        api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

        # Define image paths
        image_path_1 = Path("/home/alex/Downloads/flower.jpg")

        # Data for the API request
        data = {
            'organs': ['flower']
        }

        # Use a context manager for file handling
        with image_path_1.open('rb') as img1:
            files = [
                ('images', (image_path_1.name, img1, 'image/jpeg')),
            ]

            # Prepare and send the request
            response = requests.post(api_endpoint, files=files, data=data)

            # Handle response
            if response.status_code == 200:
                pprint(response.json())  # Pretty-print the JSON response
            else:
                print(f"Error: {response.status_code} - {response.text}")