from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from account.models import Notification
from payment.models import OrderItem

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        now = timezone.now()
        target_time = now + timedelta(hours=8)

        items = OrderItem.objects.filter(
            booked_till__range=(now, target_time)
        )

        for item in items:
            Notification.objects.create(
                user=item.order.user,
                title=f"Only 8 hours left for {item.product.name}"
            )

        self.stdout.write("Reminder notifications sent")