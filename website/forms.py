from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django_select2.forms import ModelSelect2Widget
from django import forms
from .models import *

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	address = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
	Phone_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))

	class Meta:
		model = CustomUser
		fields = ('username', 'first_name', 'last_name','address','Phone_number', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	


class AddRecordForm(forms.ModelForm):
	first_name= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),label='')
	last_name=forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),label='')
	email= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}),label='')
	phone= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mobile'}),label='')
	address= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),label='')
	city= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'city'}),label='')
	state= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),label='')
	zipcode= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip code'}),label='')

	class Meta:
		model = Record
		exclude = ("user",)


class AddCompanyForm(forms.ModelForm):
	Company_name= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Company Name'}),label='')
	Address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),label='')
# required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),label=''
	class Meta:
		model = Company
		exclude = ("user",)

# class AddProductForm(forms.ModelForm):
# 	Category_choices = [
# 		('Pesticide','Pesticide'),
# 		('Fungicide','Fungicide'),
# 		('Fertilizer','Fertilizer'),
# 		('Herbicide','Herbicide'),
# 		('Seeds','Seeds'),
# 		('Bio','Bio')
# 					 ]
# 	# Unit_choices = [
# 	# 	('1','Kg'),
# 	# 	('2','Grms'),
# 	# 	('3','Lts'),
# 	# 	('4','Mls')
# 	# ]
# 	initial = '1'
# 	Name= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Product Name'}),label='')
# 	Description=forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}),label='')
# 	hsn_code= forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'HSN Code'}),label='')
# 	Category= forms.ChoiceField(choices=Category_choices,initial=initial,label='',widget=forms.Select(attrs={'style': 'width: 200px;'}))
# 	Manufacturer= forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Manufacturer'}),label='')
# 	# Packaging_Size= forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Packaging Size'}),label='')
# 	# Unit= forms.ChoiceField(choices=Unit_choices,initial=initial,label='',widget=forms.Select(attrs={'style': 'width: 200px;'}))
# 	Formula= forms.CharField(required=True,max_length=250,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Formula'}),label='')
# 	# Usage_Instructions= forms.CharField(required=True,max_length=250,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'How to use..'}),label='')

# 	class Meta:
# 		model = Product
# 		exclude = ("user",)


class AddProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['Name', 'Description', 'hsn_code', 'Category', 'Manufacturer', 'Formula']
		# Manufacturer = forms.ModelChoiceField(queryset=Company.objects.all(), to_field_name="Company_name")
		widgets = {
            'Name': forms.TextInput(attrs={'placeholder': 'Product Name', 'style': 'width: 100%;'}),
            'Description': forms.TextInput(attrs={'placeholder': 'Description of product', 'style': 'width: 100%;'}),
            'hsn_code': forms.TextInput(attrs={'placeholder': 'hsn code', 'style': 'width: 100%;'}),
            'Category': forms.Select(attrs={'style': 'width: 100%;'}),
            'Manufacturer': forms.Select(attrs={'style': 'width: 100%;'}),
            'Formula': forms.TextInput(attrs={'placeholder': 'Formula', 'style': 'width: 100%;'}),
        }
		labels = {
            'Name': '',
            'Description': '',
            'hsn_code': '',
            'Category': '',
            'Manufacturer': '',
            'Formula': '',
        }
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['Manufacturer'].queryset = Company.objects.all()


class AddPriceForm(forms.ModelForm):
	class Meta:
		model = Price
		fields = ['Product','Batch_No', 'Size', 'Unit','MRP','Befor_Tax_price','Cost_Price'
			# ,'CGST','SGST'
			,'Profit_percentage','Selling_Price'
			]
		widgets = {
            'Product': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Product here.'}),
			'Batch_No': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Batch code'}),
            'Size': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Packaging Size(1,2..)'}),
            'Unit': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Kgs or Grms'}), 
			'MRP': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Maximum Retail Price'}),
			'Befor_Tax_price': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Before Tax Price'}),
			'Cost_Price': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Cost Price'}),
			# 'CGST': forms.TextInput(attrs={'placeholder': 'CGST %','style': 'width: 100%;'}),
			# 'SGST': forms.TextInput(attrs={'placeholder': 'SGST %','style': 'width: 100%;'}),
			'Profit_percentage': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Profit Percentage (%)','oninput': 'calculateSellingPrice();'}),
			'Selling_Price': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Selling Price'}),
        }
		labels = {
            'Product': 'Product',
			'Batch_No': 'Batch No',
            'Size': 'Size',
            'Unit': 'Unit',
			'MRP': 'MRP',
			'Befor_Tax_price':'Befor Tax Price',
			'Cost_Price': 'Cost Price',
			# 'CGST': '',
			# 'SGST': '',
			'Profit_percentage':'Profit Percentage',
			'Selling_Price': 'Selling Price',
			}
		required = {
			'Product':True,
			'Batch_No':True
		}
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['Product'].queryset = Product.objects.none()
		for field in self.fields.values():
			field.required = False
		
		if 'Product' in self.data:
			self.fields['Product'].queryset = Product.objects.all()
		elif self.instance and self.instance.pk:
			self.fields['Product'].queryset = Product.objects.all()
			self.fields['Product'].initial = self.instance.Product
		


class AddSymptomForm(forms.ModelForm):
	class Meta:
		model = symptom
		fields = ['disease_name','disease_type', 'low_sev_formula', 'low_sev_quant','low_sev_unit','med_sev_formula','med_sev_quant','med_sev_unit','high_sev_formula','high_sev_quant','high_sev_unit']
		# low_sev_formula = forms.ModelChoiceField(queryset=Product.objects.all(), to_field_name="Formula")

		widgets = {
            'disease_name': forms.TextInput(attrs={'placeholder': 'Enter Disease Name','style': 'width: 60%; margin-left: 110px;'}),
			'disease_type': forms.Select(attrs={'style': 'width: 60%; margin-left: 120px;'}),
            'low_sev_formula': forms.Select(attrs={'style': 'width: 70%;'}),
            'low_sev_quant': forms.TextInput(attrs={'placeholder':'Please enter qunatity','style': 'width: 60%; margin-left: 30px;'}), 
			'low_sev_unit': forms.Select(attrs={'style': 'width: 60%; margin-left: 60px;'}),
			'med_sev_formula': forms.Select(attrs={'style': 'width: 70%;'}),
			'med_sev_quant': forms.TextInput(attrs={'placeholder':'Please enter qunatity','style': 'width: 60%; margin-left: 30px;'}),
			'med_sev_unit': forms.Select(attrs={'style': 'width: 60%; margin-left: 60px;'}),
			'high_sev_formula': forms.Select(attrs={'style': 'width: 70%;'}),
			'high_sev_quant': forms.TextInput(attrs={'placeholder':'Please enter qunatity','style': 'width: 60%; margin-left: 30px;'}),
			'high_sev_unit': forms.Select(attrs={'style': 'width: 60%; margin-left: 60px;'}),
        }
		labels = {
            'disease_name': 'Disease Name',
			'disease_type': 'Disease Type',
            'low_sev_formula': 'Low Severity Formula',
            'low_sev_quant': 'Low Severity Quantity/Acre',
			'low_sev_unit': 'Low Severity Unit/Acre',
			'med_sev_formula': 'Med Severity Formula',
			'med_sev_quant': 'Med Severity Quantity/Acre',
			'med_sev_unit': 'Med Severity Unit/Acre',
			'high_sev_formula':'High Severity Formula',
			'high_sev_quant': 'High Severity Quantity/Acre',
			'high_sev_unit': 'High Severity Unit/Acre',
			}
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['low_sev_formula'].queryset = Product.objects.all()
		self.fields['med_sev_formula'].queryset = Product.objects.all()
		self.fields['high_sev_formula'].queryset = Product.objects.all()
		
		if self.instance and self.instance.pk:
			self.fields['low_sev_formula'].initial = self.instance.low_sev_formula
			self.fields['med_sev_formula'].initial = self.instance.med_sev_formula
			self.fields['high_sev_formula'].initial = self.instance.high_sev_formula

class PI_InvoiceForm(forms.ModelForm):
	class Meta:
		model = PI_Invoice_info
		fields = ['Invoice_Id', 'Invoice_Date', 'Company_Name', 'Address']
		widgets = {
			'Invoice_Id':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Invoice Id',}),
			'Invoice_Date':forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Company_Name': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Company Name'}),
			'Address': forms.TextInput(attrs={'class': 'form-control'}),
		}

		labels ={
			'Invoice_Id': 'Invoice Id',
			'Invoice_Date' : 'Invoice Date',
			'Company_Name': 'Company Name',
			'Address': 'Address',}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Company_Name'].queryset = Company.objects.all()

class PI_ProductForm(forms.ModelForm):
	class Meta:
		Unit_choices = [
        ('Kg','Kg'),
		('Grms','Grms'),
		('Lts','Lts'),
		('Mls','Mls')
		]
		model = PI_Product_info
		fields = [
            'Product_Name', 'Batch_No', 'Manufacture_date', 'Expiry_date',
            'Size', 'Unit', 'Quantity', 'BT_Rate', 'BT_Final_Amount',
            'CGST', 'SGST', 'PU_Final_Amount'
        ]
		widgets = {
			'Product_Name': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Product Name'}),
			'Batch_No': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Batch No'}),
			'Manufacture_date': forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Expiry_date': forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Size': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Size',}),
			'Unit': forms.Select(attrs={'class': 'form-control','placeholder': 'Select unit',},choices=Unit_choices),
			'Quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Quantity',}),
			'BT_Rate': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Before Tax Rate/Unit',}),
			'BT_Final_Amount': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Before Tax Final Amount',}),
			'CGST': forms.TextInput(attrs={'class': 'form-control','placeholder': 'CGST',}),
			'SGST': forms.TextInput(attrs={'class': 'form-control','placeholder': 'SGST',}),
			'PU_Final_Amount': forms.TextInput(attrs={'class': 'form-control','placeholder': 'After Tax Final Amount',}),
        }

		labels = {
			'Product_Name': 'Product Name',
			'Batch_No': 'Batch No',
			'Manufacture_date' : 'Manufacture Date',
			'Expiry_date': 'Expiry Date',
			'Size' : 'Size',
			'Unit' : 'Unit',
			'Quantity' : 'Quantity',
			'BT_Rate' : 'Before Tax Rate/Unit',
			'BT_Final_Amount' : 'Before Tax Final Amount',
			'CGST' : 'CGST',
			'SGST' : 'SGST',
			'PU_Final_Amount': 'After Tax Final Amount'
		}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Product_Name'].queryset = Product.objects.all()

class PI_ProductUpdateForm(forms.ModelForm):
	class Meta:
		Unit_choices = [
        ('Kg','Kg'),
		('Grms','Grms'),
		('Lts','Lts'),
		('Mls','Mls')
		]
		model = PI_Product_info
		fields = [
            'Product_Name', 'Batch_No', 'Manufacture_date', 'Expiry_date',
            'Size', 'Unit', 'Quantity', 'BT_Rate', 'BT_Final_Amount',
            'CGST', 'SGST', 'PU_Final_Amount'
        ]
		widgets = {
			'Product_Name': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Product Name'}),
			'Batch_No': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Batch No'}),
			'Manufacture_date': forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Expiry_date': forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Size': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Size',}),
			'Unit': forms.Select(attrs={'class': 'form-control','placeholder': 'Select unit',},choices=Unit_choices),
			'Quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Quantity',}),
			'BT_Rate': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Before Tax Rate/Unit',}),
			'BT_Final_Amount': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Before Tax Final Amount',}),
			'CGST': forms.TextInput(attrs={'class': 'form-control','placeholder': 'CGST',}),
			'SGST': forms.TextInput(attrs={'class': 'form-control','placeholder': 'SGST',}),
			'PU_Final_Amount': forms.TextInput(attrs={'class': 'form-control','placeholder': 'After Tax Final Amount',}),
        }

		labels = {
			'Product_Name': 'Product Name',
			'Batch_No': 'Batch No',
			'Manufacture_date' : 'Manufacture Date',
			'Expiry_date': 'Expiry Date',
			'Size' : 'Size',
			'Unit' : 'Unit',
			'Quantity' : 'Quantity',
			'BT_Rate' : 'Before Tax Rate/Unit',
			'BT_Final_Amount' : 'Before Tax Final Amount',
			'CGST' : 'CGST',
			'SGST' : 'SGST',
			'PU_Final_Amount': 'After Tax Final Amount'
		}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Product_Name'].queryset = Product.objects.all()
			for field in self.fields.values():
				field.required = False
				
class PI_PriceForm(forms.ModelForm):
	class Meta:
		model = PI_Purchase_Price
		fields = [
			# 'Invoice_Id',
			'Final_Amount',
			'Additions',
			'Deductions',
			'Revised_Amount',
			'Comments',
		]
		widgets = {
			# 'Invoice_Id': forms.TextInput(attrs={'class': 'form-control'}),
			'Final_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Additions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Deductions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Revised_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Comments': forms.Textarea(attrs={'class':'form-control','placeholder':"Leave a comment here" ,'style':"height: 100px"})
		}
		labels = {
			# 'Invoice_Id': 'Invoice Id',
			'Final_Amount': "Final Amount" ,
			'Additions' : "Additions",
			'Deductions' :"Deductions",
			'Revised_Amount': 'Revised Amount',
			'Comments': " Comments"
		}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Additions'].required = False
			self.fields['Deductions'].required = False
			self.fields['Comments'].required = False



class RI_InvoiceForm(forms.ModelForm):
	class Meta:
		model = RI_Invoice_Info
		fields = ['Return_Id', 'Return_Date', 'To_Company_Name', 'To_Address','From_Company_Name','From_Address']
		widgets = {
			'Return_Id':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Invoice Id',}),
			'Return_Date':forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'To_Company_Name': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Company Name'}),
			'To_Address': forms.TextInput(attrs={'class': 'form-control'}),
			'From_Company_Name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your Company Name'}),
			'From_Address': forms.TextInput(attrs={'class': 'form-control'}),
		}

		labels ={
			'Return_Id': 'Return Id',
			'Return_Date' : 'Return Date',
			'To_Company_Name': 'Company Name',
			'To_Address': 'Company Address',
			'From_Company_Name': 'Business Name',
			'From_Address': 'Business Address'}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['To_Company_Name'].queryset = Company.objects.all()

class RI_ProductForm(forms.ModelForm):
	class Meta:
		Unit_choices = [
        ('Kg','Kg'),
		('Grms','Grms'),
		('Lts','Lts'),
		('Mls','Mls')
		]
		model = RI_Product_Info
		fields = [
            'Product_Name', 'Batch_No', 'Manufacture_date', 'Expiry_date',
            'Size', 'Unit', 'Quantity', 'BT_Rate', 'BT_Final_Amount',
            'CGST', 'SGST', 'PU_Final_Amount'
        ]
		widgets = {
			'Product_Name': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Product Name'}),
			'Batch_No': forms.Select(attrs={'class': 'form-control','placeholder': 'Enter Batch No'}),
			'Manufacture_date': forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Expiry_date': forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Size': forms.Select(attrs={'class': 'form-control','placeholder': 'Enter Size',}),
			'Unit': forms.Select(attrs={'class': 'form-control','placeholder': 'Select unit',},choices=Unit_choices),
			'Quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Quantity',}),
			'BT_Rate': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Before Tax Rate/Unit',}),
			'BT_Final_Amount': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Before Tax Final Amount',}),
			'CGST': forms.TextInput(attrs={'class': 'form-control','placeholder': 'CGST',}),
			'SGST': forms.TextInput(attrs={'class': 'form-control','placeholder': 'SGST',}),
			'PU_Final_Amount': forms.TextInput(attrs={'class': 'form-control','placeholder': 'After Tax Final Amount',}),
        }

		labels = {
			'Product_Name': 'Product Name',
			'Batch_No': 'Batch No',
			'Manufacture_date' : 'Manufacture Date',
			'Expiry_date': 'Expiry Date',
			'Size' : 'Size',
			'Unit' : 'Unit',
			'Quantity' : 'Quantity',
			'BT_Rate' : 'Before Tax Rate/Unit',
			'BT_Final_Amount' : 'Before Tax Final Amount',
			'CGST' : 'CGST',
			'SGST' : 'SGST',
			'PU_Final_Amount': 'After Tax Final Amount'
		}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Product_Name'].queryset = Product.objects.all()

class RI_PriceForm(forms.ModelForm):
	class Meta:
		model = RI_Price_Info
		fields = [
			# 'Invoice_Id',
			'Final_Amount',
			'Additions',
			'Deductions',
			'Revised_Amount',
			'Comments',
		]
		widgets = {
			# 'Invoice_Id': forms.TextInput(attrs={'class': 'form-control'}),
			'Final_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Additions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Deductions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Revised_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Comments': forms.Textarea(attrs={'class':'form-control','placeholder':"Leave a comment here" ,'style':"height: 100px"})
		}
		labels = {
			# 'Invoice_Id': 'Invoice Id',
			'Final_Amount': "Final Amount" ,
			'Additions' : "Additions",
			'Deductions' :"Deductions",
			'Revised_Amount': 'Revised Amount',
			'Comments': " Comments"
		}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Additions'].required = False
			self.fields['Deductions'].required = False
			self.fields['Comments'].required = False

class Sales_InvoiceForm(forms.ModelForm):
	class Meta:
		model = Sales_Invoice_Info
		fields = ['Sale_Id', 'Sale_Date', 'Customer_Name', 'Address','Mobile_No','City','Expected_Payment_Date']
		widgets = {
			'Sale_Id':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Sale Id',}),
			'Sale_Date':forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Customer_Name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Select Customer Name'}),
			'Address': forms.TextInput(attrs={'class': 'form-control'}),
			'Mobile_No': forms.Select(attrs={'class': 'form-control','placeholder': 'Mobile No'}),
			'City': forms.TextInput(attrs={'class': 'form-control'}),
			'Expected_Payment_Date': forms.DateInput(attrs={'class':"form-control",'type':'date'})
		}

		labels ={
			'Sale_Id': 'Sale Id',
			'Sale_Date' : 'Sale Date',
			'Customer_Name': 'Customer Name',
			'Address': 'Address',
			'Mobile_No': 'Mobile No',
			'City': 'City',
			'Expected_Payment_Date':'Expected Payment Date'
			}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Customer_Name'].queryset = Record.objects.all()

class Sales_ProductForm(forms.ModelForm):
	class Meta:
		Unit_choices = [
        ('Kg','Kg'),
		('Grms','Grms'),
		('Lts','Lts'),
		('Mls','Mls')
		]

		model = Sales_Product_Info
		fields = [
            'Company_Name','Product_Name', 'Batch_No','Category', 'Manufacture_date', 'Expiry_date',
            'Size', 'Unit', 'Quantity', 'Retail_Price', 'Total_Price',
        ]
		widgets = {
			'Company_Name':forms.Select(attrs={'class': 'form-control','placeholder': 'Select Company Name', 'required': 'required'}),
			'Product_Name': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Product Name', 'required': 'required'}),
			'Batch_No': forms.Select(attrs={'class': 'form-control','placeholder': 'Enter Batch No', 'required': 'required'}),
			'Category':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Category', 'required': 'required'}),
			'Manufacture_date': forms.DateInput(attrs={'class':"form-control",'type':'date', 'required': 'required'}),
			'Expiry_date': forms.DateInput(attrs={'class':"form-control",'type':'date', 'required': 'required'}),
			'Size': forms.Select(attrs={'class': 'form-control','placeholder': 'Enter Size', 'required': 'required'}),
			'Unit': forms.Select(attrs={'class': 'form-control','placeholder': 'Select unit', 'required': 'required'}),
			'Quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Quantity', 'required': 'required'}),
			'Retail_Price': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Retail Price', 'required': 'required'}),
			'Total_Price': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Total Price', 'required': 'required'}),
        }

		labels = {
			'Company_Name': 'Company Name',
			'Product_Name': 'Product Name',
			'Batch_No': 'Batch No',
			'Category': 'Category',
			'Manufacture_date' : 'Manufacture Date',
			'Expiry_date': 'Expiry Date',
			'Size' : 'Size',
			'Unit' : 'Unit',
			'Quantity' : 'Quantity',
			'Retail_Price' : 'Retail Price',
			'Total_Price' : 'Total Price'
		}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Product_Name'].queryset = Product.objects.all()

class Sales_PriceForm(forms.ModelForm):
	class Meta:
		model = Sales_Price_Info
		fields = [
			# 'Invoice_Id',
			'Aggregate_Sale_Amount',
			'Additions',
			'Deductions',
			'Revised_Amount',
			'Partial_Payment',
			'Due_Payment',
			'Comments',
		]
		widgets = {
			# 'Invoice_Id': forms.TextInput(attrs={'class': 'form-control'}),
			'Aggregate_Sale_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Additions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Deductions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Revised_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Partial_Payment':forms.NumberInput(attrs={'class': 'form-control'}),
			'Due_Payment': forms.NumberInput(attrs={'class': 'form-control'}),
			'Comments': forms.Textarea(attrs={'class':'form-control','placeholder':"Leave a comment here" ,'style':"height: 100px"})
		}
		labels = {
			# 'Invoice_Id': 'Invoice Id',
			'Aggregate_Sale_Amount': "Aggregate Sale Amount" ,
			'Additions' : "Additions",
			'Deductions' :"Deductions",
			'Revised_Amount': 'Revised Amount',
			'Partial_Payment':'Partial Payment',
			'Due_Payment':'Due Payment',
			'Comments': " Comments"
		}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Additions'].required = False
			self.fields['Deductions'].required = False
			self.fields['Comments'].required = False

class Sales_RI_InvoiceForm(forms.ModelForm):
	class Meta:
		model = Sales_Return_Invoice_Info
		fields = ['Sale_Return_Id', 'Sale_Return_Date', 'Customer_Name', 'Address','Mobile_No','City']
		widgets = {
			'Sale_Return_Id':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Sale Id',}),
			'Sale_Return_Date':forms.DateInput(attrs={'class':"form-control",'type':'date'}),
			'Customer_Name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Customer Name'}),
			'Address': forms.TextInput(attrs={'class': 'form-control'}),
			'Mobile_No': forms.Select(attrs={'class': 'form-control','placeholder': 'Mobile No'}),
			'City': forms.TextInput(attrs={'class': 'form-control'})
		}

		labels ={
			'Sale_Return_Id': 'Sale Return Id',
			'Sale_Return_Date' : 'Sale Return Date',
			'Customer_Name': 'Customer Name',
			'Address': 'Address',
			'Mobile_No': 'Mobile No'
			}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Mobile_No'].queryset = Company.objects.all()

class Sales_RI_PriceForm(forms.ModelForm):
	class Meta:
		model = Sales_Return_Price_Info
		fields = [
			# 'Invoice_Id',
			'Aggregate_Return_Amount',
			'Additions',
			'Deductions',
			'Revised_Amount',
			'Comments',
		]
		widgets = {
			# 'Invoice_Id': forms.TextInput(attrs={'class': 'form-control'}),
			'Aggregate_Return_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Additions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Deductions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Revised_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Comments': forms.Textarea(attrs={'class':'form-control','placeholder':"Leave a comment here" ,'style':"height: 100px"})
		}
		labels = {
			# 'Invoice_Id': 'Invoice Id',
			'Aggregate_Return_Amount': "Aggregate Amount" ,
			'Additions' : "Additions",
			'Deductions' :"Deductions",
			'Revised_Amount': 'Revised Amount',
			'Comments': " Comments"
		}
		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['Additions'].required = False
			self.fields['Deductions'].required = False
			self.fields['Comments'].required = False