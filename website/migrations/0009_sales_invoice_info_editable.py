# Generated by Django 5.0.6 on 2024-09-08 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_alter_sales_price_info_additions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales_invoice_info',
            name='Editable',
            field=models.CharField(default=0, max_length=1),
        ),
    ]
