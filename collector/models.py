from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"

class Plot(models.Model):
    code = models.CharField(max_length=200)
    source = models.CharField(max_length=20, blank=False, null=False, default="system")

    class Meta:
        verbose_name = _('Plot')
        verbose_name_plural = _('Plots')

    def __str__(self):
        return self.code

class Observation(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    plot = models.ForeignKey(Plot, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default=None)
    geo_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default=None)
    geo_lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default=None)
    block = models.CharField(max_length=20, blank=True, null=True, default=None)
    row = models.CharField(max_length=20, blank=True, null=True, default=None)
    fertilization = models.BooleanField(default=False, blank=False, null=False)
    cutting = models.BooleanField(default=False, blank=False, null=False)
    chlorophyl = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    fungal_disease = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    eat_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    soil_moisture = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    electric_conductivity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    notes = models.TextField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('Observation')
        verbose_name_plural = _('Observations')
        ordering = ['-create_date']

    def __str__(self):
        return f"{self.user.username}-{self.create_date.strftime('%Y%m%d_%H%M%S')}"


class Species(models.Model):
    name = models.CharField(max_length=200)
    user_generated = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = _('Species')
        verbose_name_plural = _('Species')
        indexes = [models.Index(fields=['name']),]

    def __str__(self):
        return self.name


class ObservationSpecies(models.Model):
    observation = models.ForeignKey(Observation, null=False, related_name="observationspecies", on_delete=models.CASCADE)
    species = models.ForeignKey(Species, null=True, on_delete=models.CASCADE)
    coverage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('ObservationSpecies')
        verbose_name_plural = _('ObservationSpecies')


class PlotProperties(models.Model):
    plot = models.ForeignKey(Plot, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Plot Property')
        verbose_name_plural = _('Plot Properties')


