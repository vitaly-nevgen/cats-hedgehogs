import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cats_hedgehogs.settings')

application = get_wsgi_application()
