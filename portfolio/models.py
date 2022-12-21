from django.db import models

# Create your models here.
class PersonalInfo(models.Model):
    name=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural="personal Info"