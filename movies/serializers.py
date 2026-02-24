"""
Serializers for Movie Database API
Converts models to JSON and validates data
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import models
from .models import Movie, Genre, Review, Watchlist, Favorite


# =========================
# GENRE SERIALIZER
# =========================
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'created_at']


# =========================
# MOVIE SERIALIZER
# =========================
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'overview',
            'release_date',
            'vote_average',
            'vote_count',
            'poster_path',
            'backdrop_path',
            'runtime',
            'genres',
            'genre_ids',
            'tmdb_id',
            'average_rating',
            'review_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    # ⭐ Calculate average rating
    def get_average_rating(self, obj):
        if obj.reviews.exists():
            avg = obj.reviews.aggregate(avg=models.Avg('rating'))['avg']
            return round(avg, 1) if avg else None
        return None

    # ⭐ Count reviews
    def get_review_count(self, obj):
        return obj.reviews.count()

    # CREATE movie
    def create(self, validated_data):
        genre_ids = validated_data.pop('genre_ids', [])
        movie = Movie.objects.create(**validated_data)

        if genre_ids:
            movie.genres.set(genre_ids)

        return movie

    # UPDATE movie
    def update(self, instance, validated_data):
        genre_ids = validated_data.pop('genre_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if genre_ids is not None:
            instance.genres.set(genre_ids)

        return instance


# =========================
# REVIEW SERIALIZER
# =========================
class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(
        source='movie.title',
        read_only=True
    )

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'movie',
            'movie_title',
            'user',
            'rating',
            'comment',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'movie',
            'user',
            'created_at',
            'updated_at'
        ]


# =========================
# WATCHLIST SERIALIZER
# =========================
class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        write_only=True,
        source='movie'
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'movie_id', 'added_at']
        read_only_fields = ['id', 'added_at']


# =========================
# FAVORITE SERIALIZER
# =========================
class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        write_only=True,
        source='movie'
    )

    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'movie_id', 'added_at']
        read_only_fields = ['id', 'added_at']


# =========================
# USER SERIALIZER
# =========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']