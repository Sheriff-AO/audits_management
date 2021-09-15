from .models import Site, Schedule

from django.db.models.signals import post_save
from django.dispatch import receiver

# @receiver(post_save, sender=Schedule)
# def post_save_change_status(sender, instance, created, **kwargs):
#     print(sender)
#     print(instance)
#     print(created)
#     if ~created:
       
#         if site.report_received == True:
#             instance = 'Audited'