from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

RATEHAWK_CONFIG = getattr(settings, 'RATEHAWK_CONFIG', {})

if not hasattr(settings, 'RATEHAWK_CONFIG'):
    raise ImproperlyConfigured("You must define the RATEHAWK_CONFIG variable in your settings.py")

if not RATEHAWK_CONFIG.get('ID'):
    raise ImproperlyConfigured("You must define the ID attribute in your RATEHAWK_CONFIG")

if not RATEHAWK_CONFIG.get('API_KEY'):
    raise ImproperlyConfigured("You must define the API_KEY attribute in your RATEHAWK_CONFIG")
