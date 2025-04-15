# prescriptions/context_processors.py

from django.conf import settings

def media_url(request):
    """Add media URL to the context"""
    return {'MEDIA_URL': settings.MEDIA_URL}