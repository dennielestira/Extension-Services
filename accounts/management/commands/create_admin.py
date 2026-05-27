from django.core.management.base import BaseCommand
from accounts.models import CustomUser, AccountType

class Command(BaseCommand):
    help = 'Create default super admin'

    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(username='chairperson').exists():
            user = CustomUser(
                username='chairperson',
                email='admin@admin.com',
                account_type=AccountType.CAMPUS_ADMIN,
                full_name='Chairperson',
                contact_number='00000000000',
                is_superuser=True,
                is_staff=True,
            )
            user.set_password('chairperson123')
            user.save()
            self.stdout.write('Campus admin created successfully')
        else:
            self.stdout.write('Campus admin already exists')