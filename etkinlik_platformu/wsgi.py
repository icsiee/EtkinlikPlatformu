import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etkinlik_platformu.settings')

application = get_wsgi_application()
