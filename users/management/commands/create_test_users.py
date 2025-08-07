from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users for each role'

    def handle(self, *args, **options):
        test_users = [
            {
                'username': 'admin_user',
                'email': 'admin@agnovat.com',
                'password': 'admin123',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User'
            },
            {
                'username': 'support_worker',
                'email': 'worker@agnovat.com',
                'password': 'worker123',
                'role': 'worker',
                'first_name': 'Support',
                'last_name': 'Worker'
            },
            {
                'username': 'coordinator',
                'email': 'coordinator@agnovat.com',
                'password': 'coord123',
                'role': 'coordinator',
                'first_name': 'Care',
                'last_name': 'Coordinator'
            },
            {
                'username': 'practitioner',
                'email': 'practitioner@agnovat.com',
                'password': 'practice123',
                'role': 'practitioner',
                'first_name': 'Behaviour',
                'last_name': 'Practitioner'
            }
        ]

        for user_data in test_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(**user_data)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {user_data["role"]} user: {user_data["username"]}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'User {user_data["username"]} already exists'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS('\nTest users created successfully!')
        )
        self.stdout.write('You can now test the API with these credentials.')
        self.stdout.write('Visit /swagger/ for interactive API documentation.')
