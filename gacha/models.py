from django.db import models

# Create your models here.
class Characters(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    stars = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    series = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'characters'
