from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    if created:
        groups = Group.objects.filter(course=instance.course)
        if not groups.exists():
            raise ValueError("Нет доступных групп для распределения.")

        group_assignments = {group.id: group.users.count() for group in groups}
        target_group_id = min(group_assignments, key=group_assignments.get)
        group = Group.objects.get(id=target_group_id)
        group.users.add(instance.user)