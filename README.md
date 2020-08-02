# django-todo-app

Steps for setting up a django application

For creating project
django-admin startproject project_name

For creating different apps inside the project
python manage.py startapp app_name

Newly created apps must be added into settings with in parent folder
settings.py -> installed apps

For running server
python manage.py runserver

For making migrations
python manage.py makemigrations

For migrating the changes into db
python manage.py migrate

For creating super user for admin access
python manage.py createsuperuser

For updating super user password
python manage.py changepassword user_name 

Showing models inside admin
Need to register model insider admin.py for each app
from .models import ModelName
admin.site.register(ModelName)

For media and static files path need to be added in settings.py parent folder
STATIC_URL = ‘/static/’
MEDIA_ROOT = os.path.join(BASE_DIR, ‘media’)
MEDIA_URL = ‘media’

For media and static files path should be added in urls.py parent folder
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
