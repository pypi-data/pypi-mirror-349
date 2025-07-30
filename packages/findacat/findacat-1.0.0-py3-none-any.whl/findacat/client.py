import requests
from typing import Optional
from .models.cat_options import CatOptions

class FindaCat:
    def __init__(self):
        self.base_url = 'https://finda.cat'

    def get_stats(self):
        """Get the stats of the API in JSON format"""
        response = requests.get(f'{self.base_url}/stats')
        return response.json()

    def get_all_images(self):
        """Get all the image IDs in JSON format"""
        response = requests.get(f'{self.base_url}/cats/all')
        return response.json()

    def get_history(self):
        """Get the history of cat images(Base64) in JSON format"""
        response = requests.get(f'{self.base_url}/cats/history')
        return response.json()

    def get_cat(self, options: Optional[CatOptions] = None):
        """Get a random cat image with optional options"""
        url = f"{self.base_url}/cats"
        params = options.to_params() if options else {}

        response = requests.get(url, params=params)

        if response.status_code != 200:
            return response.json()
        return response
