import requests

class IMDBService:

    BASE_URL = "https://imdbapi.dev/api/titles"

    def fetch_titles(self):
        response = requests.get(self.BASE_URL)
        response.raise_for_status()
        return response.json()