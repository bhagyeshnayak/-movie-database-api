from django.shortcuts import render
import requests


def home(request):
    query = request.GET.get("q")

    movies = []

    if query:
        api_url = "http://127.0.0.1:8000/api/v1/search/"
        response = requests.get(api_url, params={"q": query})

        if response.status_code == 200:
            movies = response.json().get("results", [])

    return render(request, "index.html", {"movies": movies})