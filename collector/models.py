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
    geo_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default=None)
    geo_lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default=None)
    plot = models.CharField(max_length=20, blank=False, null=False)

class ObservationSpecies(models.Model):
    observation = models.ForeignKey(Observation, null=False, on_delete=models.CASCADE)
    species_name = models.CharField(max_length=200, blank=False, null=False)
    coverage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, default=None)



