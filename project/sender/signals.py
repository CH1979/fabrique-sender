from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from sender.models import Maillist
from sender.tasks import start_maillist


@receiver(post_save, sender=Maillist)
def start_maillist_task(sender, instance, **kwargs):
    """
    Если текущее время больше времени начала и меньше времени 
    окончания рассылки - запускаем рассылку, иначе  - ставим в очередь.
    """
    now = timezone.now()
    start_at = instance.start_at
    finish_at = instance.finish_at

    if (start_at <= now) and (finish_at > now):
        start_maillist.delay(instance.id)
    else:
        start_maillist.delay(instance.id, eta=start_at)
    return True
