from django.db import models

# Create your models here.

class Camera(models.Model):
    ip = models.GenericIPAddressField(unpack_ipv4=True, verbose_name="IP")
    name = models.CharField(max_length=150, null=True, verbose_name="Name")

