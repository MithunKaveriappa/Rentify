# In base/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, RentalRequest, Notification

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance, defaults={"full_name": instance.get_full_name() or instance.username})

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=RentalRequest)
def notify_rental_request(sender, instance, created, **kwargs):
    # Notify item owner (ACTION button) ONCE
    if created:
        if not Notification.objects.filter(
            user=instance.item.owner,
            related_request=instance,
            title="New Rental Request"
        ).exists():
            Notification.objects.create(
                user=instance.item.owner,
                title="New Rental Request",
                body=f"{instance.renter.full_name} requested your item '{instance.item.title}'.",
                link="",  # Optionally, link to the item's detail page
                related_request=instance
            )
    # Notify renter ONCE on status changes
    elif instance.status == "APPROVED":
        if not Notification.objects.filter(
            user=instance.renter,
            related_request=instance,
            title="Rental Approved"
        ).exists():
            Notification.objects.create(
                user=instance.renter,
                title="Rental Approved",
                body=f"Your request for '{instance.item.title}' was approved.",
                link="",
                related_request=instance
            )
    elif instance.status == "REJECTED":
        if not Notification.objects.filter(
            user=instance.renter,
            related_request=instance,
            title="Rental Rejected"
        ).exists():
            Notification.objects.create(
                user=instance.renter,
                title="Rental Rejected",
                body=f"Your request for '{instance.item.title}' was rejected.",
                link="",
                related_request=instance
            )
