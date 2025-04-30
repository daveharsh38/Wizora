from django.core.management.base import BaseCommand
from dashboard.models import EventReminder
from django.utils.timezone import now
from dashboard.utils import send_wish_email

class Command(BaseCommand):
    help = 'Sends birthday and anniversary wishes if today matches the reminder date.'

    def handle(self, *args, **kwargs):
        today = now().date()
        reminders = EventReminder.objects.filter(
            date__month=today.month,
            date__day=today.day
        ).exclude(year_sent=today.year)

        birthday_count = 0
        anniversary_count = 0

        for reminder in reminders:
            occasion = reminder.occasion.lower()
            if occasion in ['birthday', 'anniversary']:
                context = {
                    'sender_name': reminder.sender_name,
                    'recipient_name': reminder.recipient_name,
                    'sender_email': reminder.sender_email,
                    'recipient_email': reminder.recipient_email,
                    'location': reminder.location,
                    'custom_message': reminder.custom_message,
                    'reminder_id': reminder.id,
                    'cc': reminder.sender_email,
                }
                self.stdout.write(f"Sending {occasion} wish to {reminder.recipient_email}")
                send_wish_email(context, occasion)

                if occasion == 'birthday':
                    birthday_count += 1
                elif occasion == 'anniversary':
                    anniversary_count += 1

        self.stdout.write(self.style.SUCCESS(f"🎂 Birthday wishes sent: {birthday_count}"))
        self.stdout.write(self.style.SUCCESS(f"💍 Anniversary wishes sent: {anniversary_count}"))
        self.stdout.write(self.style.SUCCESS("✅ All applicable wishes sent successfully."))

