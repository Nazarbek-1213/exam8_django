from django.conf import settings
from django.db import models
from django.db.models import Q


class Conversation(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conv_as_user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conv_as_user2')
    project = models.ForeignKey(
        'Projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user1', 'user2', 'project')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username}"

    def other_user(self, me):
        return self.user2 if self.user1_id == me.id else self.user1

    @classmethod
    def get_or_create_between(cls, a, b, project=None):
        u1, u2 = (a, b) if a.id < b.id else (b, a)
        conv, _ = cls.objects.get_or_create(user1=u1, user2=u2, project=project)
        return conv

    @classmethod
    def for_user(cls, user):
        return cls.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-updated_at')


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"
