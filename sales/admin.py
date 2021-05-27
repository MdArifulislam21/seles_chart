from django.contrib import admin

# Register your models here.
from .models import Possition, Sale, CSV

admin.site.register(Possition)
admin.site.register(Sale)
admin.site.register(CSV)