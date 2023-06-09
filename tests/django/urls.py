from contextlib import suppress

from django.contrib.auth.models import User
from django.core.management import call_command

with suppress(Exception):
    call_command("makemigrations")
    call_command("migrate")
    if not User.objects.filter(username="x", email="user@user.com").exists():
        User.objects.create_superuser(username="x", email="user@user.com", password="x")


urlpatterns = []
