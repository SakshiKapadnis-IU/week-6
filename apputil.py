# apputil.py

import requests
import pandas as pd

class Genius:
    def __init__(self, access_token: str):
        """
        Initializes the Genius object with an access token.
        """
        self.access_token = access_token
        self.base_url = "https://api.genius.com"

    def _get_headers(self):
        """
        Returns the headers needed for API requests.
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_artist(self, search_term: str) -> dict:
        """
        Searches for an artist by name and returns a dictionary
        containing the artist's information.
        """
        search_url = f"{self.base_url}/search"
        params = {"q": search_term}
        response = requests.get(search_url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        search_data = response.json()

        # Extract primary artist ID from the first hit
        try:
            artist_id = search_data['response']['hits'][0]['result']['primary_artist']['id']
        except (IndexError, KeyError):
            return {}

        # Get full artist info
        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(artist_url, headers=self._get_headers())
        artist_response.raise_for_status()
        artist_data = artist_response.json()

        return artist_data

    def get_artists(self, search_terms: list) -> pd.DataFrame:
        """
        Takes a list of artist search terms and returns a DataFrame
        with columns: search_term, artist_name, artist_id, followers_count
        """
        rows = []

        for term in search_terms:
            artist_data = self.get_artist(term)
            
            # Safely extract artist info
            try:
                artist_info = artist_data['response']['artist']
                row = {
                    "search_term": term,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get("followers_count")
                }
            except KeyError:
                row = {
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                }

            rows.append(row)

        return pd.DataFrame(rows)