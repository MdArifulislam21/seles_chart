from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio  = models.TextField(default='no biography')
	avator = models.ImageField(upload_to = 'avators', default='no_picture.png')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}'s profile"