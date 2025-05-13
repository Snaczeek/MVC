from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Borrow

@receiver(post_save, sender=Borrow)
def update_book_status(sender, instance, created, **kwargs):
    if created:
        instance.book.is_borrowed = True
        instance.book.save()
