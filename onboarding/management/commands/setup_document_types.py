from django.core.management.base import BaseCommand
from onboarding.models import DocumentType


class Command(BaseCommand):
    help = 'Create default document types for onboarding'

    def handle(self, *args, **options):
        document_types = [
            {
                'name': 'yellow_card',
                'display_name': 'Yellow Card (Disability Worker Screening)',
                'description': 'Required disability worker screening clearance',
                'is_required': True,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'police_check',
                'display_name': 'National Police Check',
                'description': 'Criminal history check from Australian Federal Police',
                'is_required': True,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'ndis_orientation',
                'display_name': 'NDIS Orientation Certificate',
                'description': 'NDIS orientation module completion certificate',
                'is_required': True,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'first_aid',
                'display_name': 'First Aid Certificate',
                'description': 'Current first aid training certificate',
                'is_required': True,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'cpr_certificate',
                'display_name': 'CPR Certificate',
                'description': 'Cardiopulmonary resuscitation training certificate',
                'is_required': True,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'public_liability',
                'display_name': 'Public Liability Insurance',
                'description': 'Public liability insurance policy document',
                'is_required': True,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'professional_indemnity',
                'display_name': 'Professional Indemnity Insurance',
                'description': 'Professional indemnity insurance policy document',
                'is_required': True,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'car_insurance',
                'display_name': 'Car Insurance',
                'description': 'Vehicle insurance policy (if using personal vehicle)',
                'is_required': False,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'drivers_licence_front',
                'display_name': 'Driver\'s Licence (Front)',
                'description': 'Front side of current driver\'s licence',
                'is_required': False,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'jpg,jpeg,png,pdf'
            },
            {
                'name': 'drivers_licence_back',
                'display_name': 'Driver\'s Licence (Back)',
                'description': 'Back side of current driver\'s licence',
                'is_required': False,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'jpg,jpeg,png,pdf'
            },
            {
                'name': 'car_registration',
                'display_name': 'Car Registration',
                'description': 'Vehicle registration document (if using personal vehicle)',
                'is_required': False,
                'has_expiry': True,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'right_to_work',
                'display_name': 'Right to Work Check',
                'description': 'Document proving right to work in Australia',
                'is_required': True,
                'has_expiry': False,
                'max_file_size_mb': 5,
                'allowed_extensions': 'pdf,jpg,jpeg,png'
            },
            {
                'name': 'service_agreement',
                'display_name': 'Signed Service Agreement',
                'description': 'Completed and signed service agreement document',
                'is_required': True,
                'has_expiry': True,
                'max_file_size_mb': 10,
                'allowed_extensions': 'pdf'
            },
        ]

        created_count = 0
        updated_count = 0

        for doc_type_data in document_types:
            doc_type, created = DocumentType.objects.get_or_create(
                name=doc_type_data['name'],
                defaults=doc_type_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created document type: {doc_type.display_name}')
                )
            else:
                # Update existing document type
                for field, value in doc_type_data.items():
                    if field != 'name':  # Don't update the name field
                        setattr(doc_type, field, value)
                doc_type.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated document type: {doc_type.display_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDocument types setup complete!'
                f'\nCreated: {created_count}'
                f'\nUpdated: {updated_count}'
            )
        )
