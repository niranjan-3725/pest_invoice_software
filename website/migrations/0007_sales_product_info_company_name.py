# Generated by Django 5.0.6 on 2024-09-07 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_remove_record_id_alter_record_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales_product_info',
            name='Company_Name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
