from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification


def notify(user, kind, text, url=''):
    if user is None:
        return
    Notification.objects.create(user=user, kind=kind, text=text, url=url)


@receiver(post_save, sender='Bid.Bid')
def on_bid_save(sender, instance, created, **kwargs):
    from django.urls import reverse
    if created:
        notify(
            instance.project.client,
            Notification.BID,
            f"{instance.freelancer.username} {instance.project.title} loyihasiga ariza yubordi",
            reverse('project_detail', kwargs={'id': instance.project.id}),
        )
    else:
        if instance.status == 'accepted':
            notify(
                instance.freelancer,
                Notification.BID_ACCEPTED,
                f"Sizning {instance.project.title} loyihasidagi arizangiz qabul qilindi",
                reverse('project_detail', kwargs={'id': instance.project.id}),
            )
        elif instance.status == 'rejected':
            notify(
                instance.freelancer,
                Notification.BID_REJECTED,
                f"Sizning {instance.project.title} loyihasidagi arizangiz rad etildi",
                reverse('project_detail', kwargs={'id': instance.project.id}),
            )


@receiver(post_save, sender='Contracts.Contract')
def on_contract_save(sender, instance, created, **kwargs):
    from django.urls import reverse
    url = reverse('contract_detail', kwargs={'contract_id': instance.id})
    if created:
        notify(instance.freelancer, Notification.CONTRACT, f"{instance.project.title} bo'yicha shartnoma yaratildi", url)
        notify(instance.client, Notification.CONTRACT, f"{instance.project.title} bo'yicha shartnoma yaratildi", url)
    else:
        if instance.status == 'finished':
            notify(instance.freelancer, Notification.CONTRACT_FINISHED, f"{instance.project.title} shartnomasi yakunlandi", url)
        elif instance.status == 'cancelled':
            notify(instance.freelancer, Notification.CONTRACT_CANCELLED, f"{instance.project.title} shartnomasi bekor qilindi", url)


@receiver(post_save, sender='Review.Review')
def on_review_save(sender, instance, created, **kwargs):
    if created and instance.freelancer and instance.freelancer.user:
        from django.urls import reverse
        notify(
            instance.freelancer.user,
            Notification.REVIEW,
            f"Siz haqingizda yangi sharh: {instance.rating}⭐",
            reverse('review_detail', kwargs={'pk': instance.id}),
        )


@receiver(post_save, sender='Messaging.Message')
def on_message_save(sender, instance, created, **kwargs):
    if created:
        from django.urls import reverse
        recipient = instance.conversation.other_user(instance.sender)
        notify(
            recipient,
            Notification.MESSAGE,
            f"{instance.sender.username}: {instance.text[:60]}",
            reverse('conversation', kwargs={'conv_id': instance.conversation.id}),
        )
