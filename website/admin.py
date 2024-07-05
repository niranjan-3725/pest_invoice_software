from django.contrib import admin
from .models import Record,Product,Price,symptom,Company

# Register your models here.

admin.site.register(Record)

admin.site.register(Product)

admin.site.register(Price)

admin.site.register(symptom)

admin.site.register(Company)