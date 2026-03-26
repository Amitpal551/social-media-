from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from .models import FriendRequest, Message, Notification, Profile

@receiver(post_save, sender=FriendRequest)
def notify_friend_request(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.to_user,
            message=f"{instance.from_user.username} sent you a friend request."
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.to_user.id}",
            {
                "type": "notify",
                "message": f"{instance.from_user.username} sent you a friend request."
            }
        )

@receiver(post_save, sender=Message)
def notify_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=f"New message from {instance.sender.username}"
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.receiver.id}",
            {
                "type": "notify",
                "message": f"New message from {instance.sender.username}"
            }
        )

@receiver(post_save, sender=User)
def welcome_user(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            message="Welcome to the site!"
        )

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profiles.save()

