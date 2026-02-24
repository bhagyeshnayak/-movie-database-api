import requests
from movies.models import Movie, Genre


class IMDBImporter:

    URL = "https://api.imdbapi.dev/titles"

    def run(self):

        print("Fetching IMDb data...")

        response = requests.get(self.URL)
        response.raise_for_status()

        data = response.json()

        # SAFE ACCESS
        titles = data.get("titles") or data.get("results") or []

        print(f"Found {len(titles)} movies")

        for item in titles:

            movie, created = Movie.objects.get_or_create(
                title=item.get("primaryTitle", "Unknown"),
                defaults={
                    "overview": "",
                    "release_date": "2024-01-01",
                    "vote_average": item.get("rating", {}).get("aggregateRating", 0),
                    "vote_count": 0,
                    "runtime": int(item.get("runtimeSeconds", 0)) // 60,
                }
            )

            # Genres
            for g in item.get("genres", []):
                genre, _ = Genre.objects.get_or_create(name=g)
                movie.genres.add(genre)

        print("IMDb Import Finished ✅")