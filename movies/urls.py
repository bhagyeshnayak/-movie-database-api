from django.urls import path
from .views import (
    MovieListCreateView,
    MovieDetailView,
    GenreListCreateView,
    GenreDetailView,
    ReviewListCreateView,
    ReviewDetailView,
    WatchlistView,
    FavoriteView,
    ImportMovieFromTMDBView,
    ImportIMDBAPIView,
    MovieSearchView,
)

urlpatterns = [

    # ================= MOVIES =================
    path("movies/", MovieListCreateView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),

    # ================= GENRES =================
    path("genres/", GenreListCreateView.as_view()),
    path("genres/<int:pk>/", GenreDetailView.as_view()),

    # ================= REVIEWS =================
    path("movies/<int:movie_id>/reviews/", ReviewListCreateView.as_view()),
    path("reviews/<int:pk>/", ReviewDetailView.as_view()),

    # ================= WATCHLIST =================
    path("watchlist/", WatchlistView.as_view()),
    path("watchlist/<int:movie_id>/", WatchlistView.as_view()),

    # ================= FAVORITES =================
    path("favorites/", FavoriteView.as_view()),
    path("favorites/<int:movie_id>/", FavoriteView.as_view()),

    # ================= IMPORT =================
    path("movies/import/", ImportMovieFromTMDBView.as_view()),
    path("import-imdb/", ImportIMDBAPIView.as_view(), name="import-imdb"),

    # ================= SEARCH =================
  path("movies/search/", MovieSearchView.as_view(), name="movie-search"),
]