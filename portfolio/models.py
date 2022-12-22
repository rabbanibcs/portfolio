from django.db import models

# Create your models here.
class PersonalInfo(models.Model):
    name=models.CharField(max_length=100)
    about=models.TextField(null=True)

    class Meta:
        verbose_name_plural="personal Info"

    def __str__(self):
        return self.name
class Contact(models.Model):
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()

    def __str__(self):
        return self.subject