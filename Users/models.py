from django.db import models
from django.contrib.auth.models import AbstractUser

CLIENT, FREELANCER = ('client', 'freelancer')


class User(AbstractUser):
    ROLE_CHOICE = (
        (CLIENT, 'client'),
        (FREELANCER, 'freelancer'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.role}"


class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    major = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    username = models.CharField(max_length=25, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    skills = models.CharField(max_length=300, blank=True, help_text="Vergul bilan: Python, Django, React")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    portfolio_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

    def skills_list(self):
        return [s.strip() for s in (self.skills or '').split(',') if s.strip()]
