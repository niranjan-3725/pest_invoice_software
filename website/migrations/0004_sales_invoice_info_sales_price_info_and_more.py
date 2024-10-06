# Generated by Django 5.0.6 on 2024-09-05 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_ri_invoice_info_editable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales_Invoice_Info',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Sale_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Sale_Date', models.DateField()),
                ('Customer_Name', models.CharField(max_length=255)),
                ('Address', models.TextField()),
                ('Mobile_No', models.CharField(max_length=10)),
                ('City', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Sales_Invoice_Info',
            },
        ),
        migrations.CreateModel(
            name='Sales_Price_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Aggregate_Sale_Amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('Additions', models.DecimalField(decimal_places=3, max_digits=10)),
                ('Deductions', models.DecimalField(decimal_places=3, max_digits=10)),
                ('Revised_Amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('Comments', models.TextField()),
                ('Sale_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.sales_invoice_info', verbose_name='Sale_Id')),
            ],
            options={
                'db_table': 'Sale_Price_Info',
            },
        ),
        migrations.CreateModel(
            name='Sales_Product_Info',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Id', models.IntegerField()),
                ('Product_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('Batch_No', models.CharField(blank=True, max_length=255, null=True)),
                ('Manufacture_date', models.DateField(blank=True, null=True)),
                ('Expiry_date', models.DateField(blank=True, null=True)),
                ('Size', models.IntegerField(blank=True, null=True)),
                ('Unit', models.CharField(blank=True, max_length=25, null=True)),
                ('Quantity', models.IntegerField(blank=True, null=True)),
                ('Retail_Price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('Total_Price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('Combo_Pk_Id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('Combo_Id', models.CharField(max_length=255)),
                ('Sale_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.sales_invoice_info', verbose_name='Sale_Id')),
            ],
            options={
                'db_table': 'Sale_Product_info',
            },
        ),
    ]
