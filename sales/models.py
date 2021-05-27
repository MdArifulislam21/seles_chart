from django.db import models
from products.models import Products
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone
from django.shortcuts import reverse
from .utils import generate_code
# Create your models here



class Possition(models.Model):
	product = models.ForeignKey(Products, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	price = models.FloatField(blank=True)
	created = models.DateTimeField(blank=True)
	
	def save(self, *args,**kwargs):
		self.price = self.product.price * self.quantity
		return super().save(*args,**kwargs)

	def get_sales_id(self):
		sale_obj = self.sale_set.first()
		return sale_obj.id

	def get_sales_customer(self):
		sale_obj = self.sale_set.first()
		return sale_obj.customer.name

	def __str__(self):
		return f"id: {self.id}, product: {self.product.name}, quantity:{self.quantity}"

	

class Sale(models.Model):
	transaction_id = models.CharField(max_length=12, blank= True)
	position = models.ManyToManyField(Possition)
	total_price = models.FloatField(blank=True, null= True)
	customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
	salesman = models.ForeignKey(Profile, on_delete= models.CASCADE)
	created_date =models.DateTimeField(blank=True)
	updated_date = models.DateTimeField(auto_now= True)

	def __str__(self):
		return f"Sales for the amount of ${self.total_price}"

	def get_absolute_url(self):
		return reverse('sales:detail', kwargs={'pk':self.pk})

	def save(self, *args, **kwargs):
		if self.transaction_id == "":
			self.transaction_id = generate_code()

		if self.created_date is None:
			self.created_date = timezone.now()

		# positions_qs = self.position.all()
		# total_price = 0
		# for obj in positions_qs:
		# 	total_price += obj.price
		# self.total_price = total_price


		return super().save(*args, **kwargs)

	def get_positions(self):
		return self.position.all()



class CSV(models.Model):
	file_name = models.CharField(max_length=120, null=True)
	csv_file = models.FileField(upload_to='csvs', null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.file_name)

# class Possition(models.Model):
# 	pass
# 	