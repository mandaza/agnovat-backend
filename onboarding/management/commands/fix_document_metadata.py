from django.core.management.base import BaseCommand
from onboarding.models import Document


class Command(BaseCommand):
    help = 'Fix document metadata for existing documents'

    def handle(self, *args, **options):
        documents = Document.objects.all()
        fixed_count = 0
        
        for document in documents:
            needs_update = False
            
            # Fix original filename if missing
            if document.file and not document.original_filename:
                document.original_filename = document.file.name
                needs_update = True
                
            # Fix file size if missing
            if document.file and not document.file_size:
                try:
                    document.file_size = document.file.size
                    needs_update = True
                except (OSError, ValueError):
                    # File might not exist anymore
                    self.stdout.write(
                        self.style.WARNING(f'Could not get size for file: {document.file.name}')
                    )
                    document.file_size = 0
                    needs_update = True
            
            if needs_update:
                document.save()
                fixed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed metadata for document: {document.id}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nFixed {fixed_count} documents')
        )
