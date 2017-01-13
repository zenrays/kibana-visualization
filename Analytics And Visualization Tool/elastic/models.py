from django.db import models

# Create your models here.
class MobileDB(models.Model):
	name = models.CharField(max_length=30)
	brand = models.CharField(max_length=30)
	camera = models.IntegerField()
	ram = models.IntegerField()
	memory=models.IntegerField()
	battery = models.IntegerField()
	price = models.IntegerField()