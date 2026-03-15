from django.db import models
from Users.models import User, FreelancerProfile


class Review(models.Model):

    freelancer = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="freelancer_reviews"
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_reviews",
        null=True,blank=True
    )

    rating = models.IntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)