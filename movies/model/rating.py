from django.db import models

class Rating(models.Model):
    movie = models.OneToOneField(
        "Movie",
        on_delete=models.CASCADE,
        related_name="rating"
    )

    aggregate_rating = models.FloatField(null=True)