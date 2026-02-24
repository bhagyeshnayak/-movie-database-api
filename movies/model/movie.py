from django.db import models
# Create your models here.
class movie(models.model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    movie_type = models.CharField(max_length=50)
    release_year = models.IntegerField(null=True, blank=True)
    runtime_seconds = models.IntegerField(null=True, blank=True)
    poster=models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    genres = models.ManyToManyField(
    "Genre",
    related_name="movies"
)