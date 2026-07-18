from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

FIXTURE_NAME = 'demo'
FIXTURE_PATH = settings.BASE_DIR / 'core' / 'fixtures' / f'{FIXTURE_NAME}.json'


class Command(BaseCommand):
    help = (
        "Load demo/placeholder data from core/fixtures/demo.json for local "
        "development and walkthroughs. Safe to run repeatedly (Django's "
        "loaddata upserts by pk)."
    )

    def handle(self, *args, **options):
        if not FIXTURE_PATH.exists() or FIXTURE_PATH.read_text().strip() in ('', '[]'):
            self.stdout.write(self.style.WARNING(
                f"{FIXTURE_PATH} is empty. Add fixture entries and re-run this "
                "command. Example entries:\n\n"
                '  {"model": "events.event", "pk": 1, "fields": {"title": '
                '"Fall Kickoff", "date": "2026-09-05T18:00:00Z", '
                '"event_type": "MEETING", "description": "", "location": '
                '"Room 204"}},\n'
                '  {"model": "projects.project", "pk": 1, "fields": {"name": '
                '"Demo High-Altitude Balloon", "description": "Placeholder '
                'project for demos.", "status": "ACTIVE", "start_date": '
                '"2026-01-15"}}\n'
            ))
            return

        call_command('loaddata', FIXTURE_NAME)
        self.stdout.write(self.style.SUCCESS(f"Loaded fixtures from {FIXTURE_PATH}"))
