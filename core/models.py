from django.db import models


class Country(models.Model):
    name = models.CharField(unique=True, max_length=255)
    code = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    class Meta:
        unique_together = ['country', 'code']


    def __str__(self):
        return self.name
