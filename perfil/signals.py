from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from perfil.models import Perfil

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)