# Generated by Django 5.0.6 on 2024-07-09 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_pi_product_info_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pi_product_info',
            name='Combo_Id',
        ),
    ]