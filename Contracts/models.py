from django.conf import settings
from django.db import models
from Projects.models import Project


class Contract(models.Model):
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (FINISHED, "Finished"),
        (CANCELLED, "Cancelled"),
    )

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="contract"
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_contracts"
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="freelancer_contracts"
    )
    agreed_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"Contract - {self.project.title}"