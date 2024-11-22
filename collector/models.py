from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"

class Observation(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default=None)



