from django.db import models

class chatRequest(models.Model):
    request = models.CharField(max_length=100)
    def __str__(self):
        return self.request


class chatbotUser(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=12)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
# Create your models here.
