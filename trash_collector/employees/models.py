from django.db import models


# Create your models here.


class Employees(models.Model):
    name = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
