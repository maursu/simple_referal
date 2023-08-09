from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from faker import Faker

User = get_user_model()

fake = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("num_of_users", type=int)

    def handle(self, *args, **options):
        num_of_users = options["num_of_users"]
        User.objects.all().delete()

        for _ in range(num_of_users):
            user = User.objects.create_user(phone_number=fake.phone_number())
            user.set_login_code()

        self.stdout.write(f"succesfully created {num_of_users} users")
