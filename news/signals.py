from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from accounts.models import CustomUser

@receiver(m2m_changed, sender=CustomUser.groups.through)
def update_user_role(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        if instance.groups.filter(name='Escritor').exists():
            instance.role = 'Escritor'
        elif instance.groups.filter(name='Admin').exists():
            instance.role = 'Admin'
        else:
            instance.role = 'Leitor'
        instance.save()