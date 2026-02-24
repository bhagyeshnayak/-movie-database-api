"""
Movie Database Models
Production Ready Models
"""

from django.db import models
from django.contrib.auth.models import User


# =====================================================
# GENRE MODEL
# =====================================================
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# =====================================================
# MOVIE MODEL
# =====================================================
class Movie(models.Model):

    # Basic Info
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)

    release_date = models.DateField(null=True, blank=True)

    # Ratings (TMDB / IMDb)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)

    # Media
    poster_path = models.URLField(blank=True, null=True)
    backdrop_path = models.URLField(blank=True, null=True)

    runtime = models.IntegerField(default=0)

    # Relations
    genres = models.ManyToManyField(
        Genre,
        related_name="movies",
        blank=True
    )

    # External IDs (IMPORTANT ⭐)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-release_date"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["release_date"]),
        ]


# =====================================================
# REVIEW MODEL
# =====================================================
class Review(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)]
    )

    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/10)"

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["movie", "user"]


# =====================================================
# WATCHLIST MODEL
# =====================================================
class Watchlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlist"
    )

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

    class Meta:
        ordering = ["-added_at"]
        unique_together = ["user", "movie"]


# =====================================================
# FAVORITE MODEL
# =====================================================
class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

    class Meta:
        ordering = ["-added_at"]
        unique_together = ["user", "movie"]