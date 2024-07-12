from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            phone='79885685468',
            first_name='admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('123456')
        user.save()
