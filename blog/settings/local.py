from .base import *

DEBUG=True

ALLOWED_HOSTS = ['192.168.43.86','127.0.0.1','157.245.108.160']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#DEFAULT_FILE_STORAGE = "github_storages.backend.BackendStorages"
#GITHUB_HANDLE = "GAGANsinghmsitece"
#ACCESS_TOKEN = "c8eec457ce6d9223136997489d922eb1fbe8f46f"
#GITHUB_REPO_NAME = "django_blog_bucket"
#MEDIA_BUCKET_NAME = "media"
python3.7 manage.py migrate --settings=blog.settings.local