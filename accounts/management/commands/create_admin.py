from django.core.management.base import BaseCommand
from accounts.models import CustomUser, AccountType

class Command(BaseCommand):
    help = 'Create default super admin'

    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                username='chairperson',
                email='admin@admin.com',
                password='chairperson123',
                account_type=AccountType.CAMPUS_ADMIN
            )
            self.stdout.write('Super admin created successfully')
        else:
            self.stdout.write('Super admin already exists')