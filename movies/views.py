"""
Complete CRUD Views + External API Import
Movie Database API
"""

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Movie, Genre, Review, Watchlist, Favorite
from .serializers import (
    MovieSerializer,
    GenreSerializer,
    ReviewSerializer,
    WatchlistSerializer,
    FavoriteSerializer
)

from .services.tmdb_service import TMDBService
from .importers.imdb_importer import IMDBImporter


# ====================================================
# MOVIE CRUD
# ====================================================

class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        genre = request.query_params.get("genre")
        if genre:
            queryset = queryset.filter(genres__name__icontains=genre)

        year = request.query_params.get("year")
        if year:
            queryset = queryset.filter(release_date__year=year)

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        sort = request.query_params.get("sort", "-release_date")
        queryset = queryset.order_by(sort)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "results": serializer.data
        })


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "pk"


# ====================================================
# GENRE CRUD
# ====================================================

class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "pk"


# ====================================================
# REVIEW CRUD
# ====================================================

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        movie_id = self.kwargs.get("movie_id")
        return Review.objects.filter(movie_id=movie_id)

    def perform_create(self, serializer):
        movie_id = self.kwargs.get("movie_id")
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer.save(user=self.request.user, movie=movie)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "pk"

    def get_queryset(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return Review.objects.filter(user=self.request.user)
        return Review.objects.all()


# ====================================================
# WATCHLIST
# ====================================================

class WatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        watchlist = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, movie_id):
        item = get_object_or_404(
            Watchlist,
            user=request.user,
            movie_id=movie_id
        )
        item.delete()
        return Response(status=204)


# ====================================================
# FAVORITES
# ====================================================

class FavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, movie_id):
        item = get_object_or_404(
            Favorite,
            user=request.user,
            movie_id=movie_id
        )
        item.delete()
        return Response(status=204)


# ====================================================
# TMDB SINGLE MOVIE IMPORT
# ====================================================

class ImportMovieFromTMDBView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        tmdb_id = request.data.get("tmdb_id")

        if not tmdb_id:
            return Response(
                {"error": "tmdb_id required"},
                status=400
            )

        service = TMDBService()
        data = service.get_movie_details(tmdb_id)

        if "error" in data:
            return Response(data, status=404)

        movie, created = Movie.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "title": data["title"],
                "overview": data.get("overview", ""),
                "release_date": data.get("release_date"),
                "vote_average": data.get("vote_average", 0),
                "vote_count": data.get("vote_count", 0),
                "runtime": data.get("runtime", 0),
                "poster_path": data.get("poster_path", ""),
                "backdrop_path": data.get("backdrop_path", ""),
            }
        )

        serializer = MovieSerializer(movie)

        return Response({
            "message": "Movie imported" if created else "Movie exists",
            "movie": serializer.data
        })


# ====================================================
# ⭐ IMDb BULK IMPORT (NEW FEATURE)
# ====================================================

class ImportIMDBAPIView(APIView):
    """
    POST /api/v1/import-imdb/
    Import thousands of movies automatically
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        importer = IMDBImporter()
        importer.run()

        return Response({
            "message": "IMDb movies imported successfully"
        })


# ====================================================
# SEARCH MOVIES
# ====================================================

class MovieSearchView(ListAPIView):
    """
    Advanced Search API

    GET /api/v1/search/?q=batman
    GET /api/v1/search/?genre=action
    GET /api/v1/search/?q=batman&genre=action
    """
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):

        query = self.request.query_params.get("q")
        genre = self.request.query_params.get("genre")

        qs = Movie.objects.all()

        # Search by movie title
        if query:
            qs = qs.filter(title__icontains=query)

        # Filter by genre
        if genre:
            qs = qs.filter(genres__name__icontains=genre)

        return qs.distinct()