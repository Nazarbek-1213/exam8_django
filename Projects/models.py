from django.conf import settings
from django.db import models


class Project(models.Model):
    WEB = "web"
    DESIGN = "design"
    MOBILE = "mobile"
    WRITING = "writing"
    DATA = "data"
    AI = "ai"

    CATEGORY_CHOICES = [
        (WEB, "Web Development"),
        (DESIGN, "Design"),
        (MOBILE, "Mobile Development"),
        (WRITING, "Content Writing"),
        (DATA, "Data Science"),
        (AI, "AI / ML"),
    ]

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (OPEN, "Open"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    )

    FIXED = "fixed"
    HOURLY = "hourly"
    MILESTONE = "milestone"

    BUDGET_TYPE_CHOICES = [
        (FIXED, "Fixed"),
        (HOURLY, "Hourly"),
        (MILESTONE, "Milestone"),
    ]

    ENTRY = "entry"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

    LEVEL_CHOICES = [
        (ENTRY, "Entry"),
        (INTERMEDIATE, "Intermediate"),
        (EXPERT, "Expert"),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPE_CHOICES, default=FIXED)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=INTERMEDIATE)
    skills = models.TextField(blank=True, null=True)

    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title