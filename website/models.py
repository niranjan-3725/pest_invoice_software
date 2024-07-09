from django.db import models
import re
from datetime import date
# Create your models here.

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)

#This db_table sets the table name in the db
    class Meta:
        db_table = 'customers'

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")

class Company(models.Model):
    Created_at = models.DateTimeField(auto_now_add=True)
    Company_name = models.CharField(max_length=250,primary_key=True)
    Address = models.TextField()

    class Meta:
        db_table = 'company'
    def __str__(self):
        return self.Company_name
    def save(self, *args, **kwargs):
        Name_var = re.sub(r'(\d)(%|\+|\-|\*|\/)', r'\1 \2 ', self.Company_name)
        Name_var = re.sub(r'([^a-zA-Z0-9\s])', r' \1 ', Name_var)
        Name_var = ' '.join(Name_var.split())
        self.Company_name = Name_var.upper()
        #Adress Trans
        Address_var = re.sub(r'(\d)(%|\+|\-|\*|\/)', r'\1 \2 ', self.Address)
        Address_var = re.sub(r'([^a-zA-Z0-9\s])', r' \1 ', Address_var)
        Address_var = ' '.join(Address_var.split())
        self.Address = Address_var.capitalize()
        super(Company, self).save(*args, **kwargs)


    
class Product(models.Model):
    Category_choices = [
	    ('Pesticide','Pesticide'),
		('Fungicide','Fungicide'),
		('Fertilizer','Fertilizer'),
		('Herbicide','Herbicide'),
		('Seeds','Seeds'),
		('Bio','Bio')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    Name = models.CharField(max_length=100,primary_key = True)
    Description = models.TextField(null=True)
    hsn_code = models.CharField(max_length=50)
    Category = models.CharField(max_length=50,choices=Category_choices,default='Pesticide') #choiceField (Pest,Herb,fung,ferti,seed)
    Manufacturer = models.CharField(max_length=250)
    # Packaging_Size = models.IntegerField() 
    # Unit = models.CharField(max_length=50) #choiceField (Liters,Kilograms)
    Formula = models.CharField(max_length=250) #choiceField
    # Usage_Instructions = models.CharField(max_length=250,null=True)
    #zipcode = models.CharField(max_length=10)

#This db_table sets the table name in the db``
    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.Name
    def save(self, *args, **kwargs):
        Name_var = re.sub(r'(\d)(%|\+|\-|\*|\/)', r'\1 \2 ', self.Name)
        Name_var = re.sub(r'([^a-zA-Z0-9\s])', r' \1 ', Name_var)
        Name_var = ' '.join(Name_var.split())
        self.Name = Name_var.upper()
        #Formula Column Trasformation
        Fomrula_var = re.sub(r'(\d)(%|\+|\-|\*|\/)', r'\1 \2 ', self.Formula)
        Fomrula_var = re.sub(r'([^a-zA-Z0-9\s])', r' \1 ', Fomrula_var)
        Fomrula_var = ' '.join(Fomrula_var.split())
        self.Formula = Fomrula_var.upper()
        super(Product, self).save(*args, **kwargs)

        
class Price(models.Model):
    Unit_choices = [
        ('Kg','Kg'),
		('Grms','Grms'),
		('Lts','Lts'),
		('Mls','Mls')
    ]
    ID = models.CharField(primary_key=True,max_length=200,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Product = models.CharField(max_length=100)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Product')
    Batch_code = models.CharField(max_length=25)
    Packaging_Size = models.IntegerField()
    Unit = models.CharField(max_length=25,choices=Unit_choices,default='Kg')
    MRP = models.DecimalField(max_digits=10,decimal_places=3)
    Cost_Price = models.DecimalField(max_digits=10,decimal_places=3)
    CGST = models.DecimalField(max_digits=10,decimal_places=3)
    SGST = models.DecimalField(max_digits=10,decimal_places=3)
    Profit_percentage = models.DecimalField(max_digits=10,decimal_places=3)
    Selling_Price = models.DecimalField(max_digits=10,decimal_places=3)
    
    #This db_table sets the table name in the db
    class Meta:
        db_table = 'price'
    def __str__(self):
        return str(self.Product)
    def save(self, *args, **kwargs):
        self.ID = f'{self.Product}_{self.Packaging_Size}_{self.Unit}_{self.Batch_code.upper()}'
        self.Batch_code = self.Batch_code.upper()
        super(Price, self).save(*args, **kwargs)

class symptom(models.Model):
    disease_choices = [
		('Pest','Pest'),
		('Fungi','Fungi'),
		('Nematodes','Nematodes'),
        ('Bacteria','Bacteria')
    ]
    Unit_choices = [
        ('Kg','Kg'),
		('Grms','Grms'),
		('Lts','Lts'),
		('Mls','Mls')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    disease_name = models.CharField(max_length=250,primary_key = True)
    disease_type = models.CharField(max_length=15,choices=disease_choices,default='Pest')
    # low_sev_formula = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='low_sev_formula_set')
    low_sev_formula = models.CharField(max_length=250)
    low_sev_quant = models.DecimalField(max_digits=10,decimal_places=3)
    low_sev_unit = models.CharField(max_length=25,choices=Unit_choices,default='Grms')
    # med_sev_formula = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='med_sev_formula_set')
    med_sev_formula = models.CharField(max_length=250)
    med_sev_quant = models.DecimalField(max_digits=10,decimal_places=3)
    med_sev_unit = models.CharField(max_length=25,choices=Unit_choices,default='Grms')
    # high_sev_formula = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='high_sev_formula_set')
    high_sev_formula = models.CharField(max_length=250)
    high_sev_quant = models.DecimalField(max_digits=10,decimal_places=3)
    high_sev_unit = models.CharField(max_length=25,choices=Unit_choices,default='Grms')

    class Meta:
        db_table = 'symptom'
    def __str__(self):
        return str(self.disease_name)
    def save(self, *args, **kwargs):
        disease_name_var = re.sub(r'(\d)(%|\+|\-|\*|\/)', r'\1 \2 ', self.disease_name)
        disease_name_var = re.sub(r'([^a-zA-Z0-9\s])', r' \1 ', disease_name_var)
        disease_name_var = ' '.join(disease_name_var.split())
        self.disease_name = disease_name_var.upper()
        # self.low_sev_formula = Product.objects.filter(Name = self.low_sev_formula).first().Formula
        # self.med_sev_formula = Product.objects.filter(Name = self.med_sev_formula).first().Formula
        # self.high_sev_formula = Product.objects.filter(Name = self.high_sev_formula).first().Formula
        super(symptom, self).save(*args, **kwargs)

class inventory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    Product_Name = models.CharField(max_length=255)
    Batch_No = models.CharField(max_length=50)
    Size = models.IntegerField()
    Unit = models.CharField(max_length=25)
    Quantity = models.IntegerField()
    Manufacture_date = models.DateField()
    Expiry_date = models.DateField()
    Combo_Id = models.CharField(max_length=255,primary_key=True) #Product_Name_Batch_No_Size+Unit


class PI_Invoice_info(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    Invoice_Id = models.CharField(max_length=255,primary_key=True)
    Invoice_Date = models.DateField(blank=False,null=False)
    Company_Name = models.CharField(max_length=255)
    Address = models.TextField()
    class Meta:
        db_table = 'PI_Invoice_info'
    def __str__(self):
        return str(self.Invoice_Id)


class PI_Product_info(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    Invoice_Id = models.ForeignKey(PI_Invoice_info,on_delete=models.CASCADE,verbose_name='Invoice_id')
    Id = models.IntegerField()
    Product_Name = models.CharField(max_length=255)
    Batch_No = models.CharField(max_length=50)
    Manufacture_date = models.DateField()
    Expiry_date = models.DateField()
    Size = models.IntegerField()
    Unit = models.CharField(max_length=25)
    Quantity = models.IntegerField()
    BT_Rate = models.DecimalField(max_digits=10,decimal_places=3)
    BT_Final_Amount = models.DecimalField(max_digits=10,decimal_places=3)
    CGST = models.DecimalField(max_digits=10,decimal_places=3)
    SGST = models.DecimalField(max_digits=10,decimal_places=3)
    PU_Final_Amount = models.DecimalField(max_digits=10,decimal_places=3)
    Combo_Pk_Id = models.CharField(max_length=255,primary_key=True) #Invoice_Id_Product_Name_Batch_No_Size+Unit
    Combo_Id = models.CharField(max_length=255)  #Invoice_Id_Product_Name_Batch_No_Size+Unit

    class Meta:
        db_table = 'PI_Product_info'
    def __str__(self):
        return str(self.Invoice_Id)

class PI_Purchase_Price(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    Invoice_Id = models.ForeignKey(PI_Invoice_info,on_delete=models.CASCADE,verbose_name='Invoice_id')
    Final_Amount = models.DecimalField(max_digits=10,decimal_places=3)
    Additions = models.DecimalField(max_digits=10,decimal_places=3)
    Deductions = models.DecimalField(max_digits=10,decimal_places=3)
    Revised_Amount = models.DecimalField(max_digits=10,decimal_places=3)
    Comments = models.TextField()

    class Meta:
        db_table = 'PI_Purchase_Price'
    def __str__(self):
        return str(self.Invoice_Id)