from django.conf import settings
from django.db import models
from Projects.models import Project
PENDING,ACCEPTED,REJECTED=('pending','accepted','rejected')

class Bid(models.Model):

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    xabar = models.TextField()
    attachment = models.FileField(upload_to='bids/', blank=True, null=True)
    delivery_days = models.PositiveIntegerField(default=7)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "freelancer")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.freelancer.username} -> {self.project.title}"