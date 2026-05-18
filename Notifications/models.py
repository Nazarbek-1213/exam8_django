from django.conf import settings
from django.db import models


class Notification(models.Model):
    BID = 'bid'
    BID_ACCEPTED = 'bid_accepted'
    BID_REJECTED = 'bid_rejected'
    CONTRACT = 'contract'
    CONTRACT_FINISHED = 'contract_finished'
    CONTRACT_CANCELLED = 'contract_cancelled'
    REVIEW = 'review'
    MESSAGE = 'message'

    KIND_CHOICES = (
        (BID, 'Yangi ariza'),
        (BID_ACCEPTED, 'Ariza qabul qilindi'),
        (BID_REJECTED, 'Ariza rad etildi'),
        (CONTRACT, 'Shartnoma yaratildi'),
        (CONTRACT_FINISHED, 'Shartnoma tugatildi'),
        (CONTRACT_CANCELLED, 'Shartnoma bekor qilindi'),
        (REVIEW, 'Sharh qoldirildi'),
        (MESSAGE, 'Yangi xabar'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    kind = models.CharField(max_length=30, choices=KIND_CHOICES)
    text = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]}"
