from pathlib import Path
import os
from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

include(
    'components/database.py',
    'components/application.py',
    'components/pswd_validation.py',
    'components/internationalization.py',
)

INTERNAL_IPS = [
    "127.0.0.1",
]

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = ['movies/locale']
