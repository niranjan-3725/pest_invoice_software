from django.contrib import admin
from .models import *
#PI_Invoice_info,PI_Product_info

# Register your models here.

admin.site.register(CustomUser)

admin.site.register(Record)

admin.site.register(Product)

admin.site.register(Price)

admin.site.register(symptom)

admin.site.register(Company)

admin.site.register(inventory)

admin.site.register(PI_Invoice_info)
admin.site.register(PI_Product_info)
admin.site.register(PI_Purchase_Price)

admin.site.register(RI_Invoice_Info)
admin.site.register(RI_Product_Info)
admin.site.register(RI_Price_Info)