
# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
