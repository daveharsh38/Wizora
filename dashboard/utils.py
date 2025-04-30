from django.core.mail import EmailMessage
from django.conf import settings
from datetime import date
from django.utils import timezone
from dashboard.models import EventReminder, OccasionTemplate
import random

def send_wish_email(context, occasion='birthday'):
    try:
        # Check if already sent
        reminder_id = context.get("reminder_id")
        if reminder_id:
            already_sent = EventReminder.objects.filter(
                id=reminder_id, year_sent=date.today().year
            ).exists()
            if already_sent:
                print(f"[⚠️] Skipping: Already sent for reminder ID {reminder_id}")
                return

        # Select random template from database
        templates = OccasionTemplate.objects.filter(occasion=occasion)
        if not templates.exists():
            raise Exception(f"No templates found in database for occasion '{occasion}'")

        selected_template = random.choice(templates)
        template_content = selected_template.content

        # Render template with context
        message = template_content.format(
            recipient_name=context.get('recipient_name', ''),
            sender_name=context.get('sender_name', ''),
            custom_message=context.get('custom_message', '')
        )

        subject = f"🎉 Happy {occasion.capitalize()} {context.get('recipient_name', '')}!"
        recipient_email = context['recipient_email']
        sender_email = settings.DEFAULT_FROM_EMAIL
        cc_email = context.get('cc')

        # Prepare and send email
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=sender_email,
            to=[recipient_email],
        )
        if cc_email:
            email.cc = [cc_email]  # ✅ Proper CC handling (no duplicate header)
        email.send()

        print(f"[✔️] Sent {occasion} email to {recipient_email} with CC: {cc_email}")

        # Mark as sent
        if reminder_id:
            reminder = EventReminder.objects.get(id=reminder_id)
            reminder.sent = True
            reminder.sent_at = timezone.now()
            reminder.year_sent = date.today().year
            reminder.save()
            print(f"[📌] Updated EventReminder ID {reminder_id} as sent.")

    except Exception as e:
        print(f"[❌] Failed to send {occasion} email: {e}")

def reset_email_flags_for_year(target_year=None):
    if target_year is None:
        target_year = date.today().year

    updated_count = EventReminder.objects.filter(year_sent=target_year).update(
        sent=False,
        sent_at=None,
        year_sent=None
    )

    print(f"[🔄] Reset {updated_count} reminder(s) for year {target_year}")
