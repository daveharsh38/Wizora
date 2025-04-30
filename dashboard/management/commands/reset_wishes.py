from django.core.management.base import BaseCommand
from dashboard.utils import reset_email_flags_for_year


class Command(BaseCommand):
    help = '🔄 Resets the sent email flags for a specific year (or current year by default).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            help='Specify the year to reset the flags for. Defaults to current year if not provided.'
        )

    def handle(self, *args, **kwargs):
        target_year = kwargs.get('year')
        reset_email_flags_for_year(target_year)
        if target_year:
            self.stdout.write(self.style.SUCCESS(f"✅ Email flags reset for year {target_year}."))
        else:
            self.stdout.write(self.style.SUCCESS("✅ Email flags reset for the current year."))
