from django.db import models

class Customer(models.Model):
	name = models.CharField(max_length = 120)
	logo = models.ImageField(upload_to='customers', default='No_picture.png')

	def __str__(self):
		return self.name