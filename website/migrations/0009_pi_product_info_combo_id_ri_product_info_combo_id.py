# Generated by Django 5.0.6 on 2024-08-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_ri_invoice_info_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pi_product_info',
            name='Combo_Id',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ri_product_info',
            name='Combo_Id',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
