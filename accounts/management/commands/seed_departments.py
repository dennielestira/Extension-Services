from django.core.management.base import BaseCommand
from accounts.models import Department

class Command(BaseCommand):
    help = 'Seed departments'

    def handle(self, *args, **kwargs):
        for code, _ in Department.DEPARTMENT_CHOICES:
            obj, created = Department.objects.get_or_create(name=code)
            self.stdout.write(f'{"Created" if created else "Exists"}: {obj}')
        self.stdout.write(f'Total: {Department.objects.count()}')