
from django.contrib import admin
from .models import Movie, Genre, Review, Watchlist, Favorite


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "release_date", "vote_average")
    search_fields = ("title",)
    list_filter = ("release_date", "genres")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "user", "rating", "created_at")
    list_filter = ("rating",)


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "added_at")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "added_at")

# Register your models here.
