# prescriptions/management/commands/create_directories.py

import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates necessary directories for media uploads'

    def handle(self, *args, **options):
        directories = [
            settings.MEDIA_ROOT,
            settings.UPLOAD_FOLDER,
            settings.PAST_SCANS_FOLDER,
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f'Created directory: {directory}'))