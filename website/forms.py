from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django_select2.forms import ModelSelect2Widget
from django import forms
from .models import Record,Product,Price,symptom,Company,PI_Invoice_info,PI_Product_info,PI_Purchase_Price

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


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
		fields = ['Product','Batch_code', 'Packaging_Size', 'Unit','MRP','Cost_Price','CGST','SGST','Profit_percentage','Selling_Price']
		widgets = {
            'Product': forms.Select(attrs={'placeholder': 'Select Product here.','style': 'width: 100%;'}),
			'Batch_code': forms.TextInput(attrs={'placeholder': 'Batch code','style': 'width: 100%;'}),
            'Packaging_Size': forms.TextInput(attrs={'placeholder': 'Packaging Size(1,2..)','style': 'width: 100%;'}),
            'Unit': forms.Select(attrs={'placeholder': 'Select Kgs or Grms','style': 'width: 100%;'}), 
			'MRP': forms.TextInput(attrs={'placeholder': 'Maximum Retail Price','style': 'width: 100%;'}),
			'Cost_Price': forms.TextInput(attrs={'placeholder': 'Cost Price','style': 'width: 100%;'}),
			'CGST': forms.TextInput(attrs={'placeholder': 'CGST %','style': 'width: 100%;'}),
			'SGST': forms.TextInput(attrs={'placeholder': 'SGST %','style': 'width: 100%;'}),
			'Profit_percentage': forms.TextInput(attrs={'placeholder': 'Profit Percentage (%)','style': 'width: 100%;','oninput': 'calculateSellingPrice();'}),
			'Selling_Price': forms.TextInput(attrs={'placeholder': 'Selling Price','style': 'width: 100%;'}),
        }
		labels = {
            'Product': 'Product',
			'Batch_code': '',
            'Packaging_Size': '',
            'Unit': '',
			'MRP': '',
			'Cost_Price': '',
			'CGST': '',
			'SGST': '',
			'Profit_percentage':'',
			'Selling_Price': '',
			}
		required = {
			'Product':True,
			'Batch_code':True
		}
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['Product'].queryset = Product.objects.none()
		
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

# class AddPruchaseInvoiceForm(forms.ModelForm):
# 	class Meta:
# 		Unit_choices = [
#         ('Kg','Kg'),
# 		('Grms','Grms'),
# 		('Lts','Lts'),
# 		('Mls','Mls')
# 		]
# 		model = purchase_invoice
# 		fields = ['Invoice_Id','Invoice_Date','Company_Name','Address','Product_Name','Batch_No','Manufacture_date','Expiry_date'
# 			,'Size','Unit','Quantity','BT_Rate','BT_Final_Amount','CGST','SGST','PU_Final_Amount'
# 			]
# 		widgets = {
# 			'Invoice_Id':forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Invoice Id',}),
# 			'Invoice_Date':forms.DateInput(attrs={'class':"form-control",'type':'date'}),
# 			'Company_Name': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Company Name'}),
# 			'Address': forms.TextInput(attrs={'class': 'form-control'}),
# 			'Product_Name': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Product Name'}),
# 			'Batch_No': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Batch No'}),
# 			'Manufacture_date': forms.DateInput(attrs={'class':"form-control",'type':'date'}),
# 			'Expiry_date': forms.DateInput(attrs={'class':"form-control",'type':'date'}),
# 			'Size': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Size',}),
# 			'Unit': forms.Select(attrs={'class': 'form-control','placeholder': 'Select unit',},choices=Unit_choices),
# 			'Quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter Quantity',}),
# 			'BT_Rate': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Before Tax Rate/Unit',}),
# 			'BT_Final_Amount': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Before Tax Final Amount',}),
# 			'CGST': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'CGST',}),
# 			'SGST': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'SGST',}),
# 			'PU_Final_Amount': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'After Tax Final Amount',})
# 		}

# 		labels ={
# 			'Invoice_Id': 'Invoice Id',
# 			'Invoice_Date' : 'Invoice Date',
# 			'Company_Name': 'Company Name',
# 			'Address': 'Address',
# 			'Product_Name': 'Product Name',
# 			'Batch_No': 'Batch No',
# 			'Manufacture_date' : 'Manufacture Date',
# 			'Expiry_date': 'Expiry Date',
# 			'Size' : 'Size',
# 			'Unit' : 'Unit',
# 			'Quantity' : 'Quantity',
# 			'BT_Rate' : 'Before Tax Rate/Unit',
# 			'BT_Final_Amount' : 'Before Tax Final Amount',
# 			'CGST' : 'CGST',
# 			'SGST' : 'SGST',
# 			'PU_Final_Amount': 'After Tax Final Amount'
# 		}

# 		def __init__(self,*args,**kwargs):
# 			super().__init__(*args,**kwargs)
# 			self.fields['Company_Name'].queryset = Company.objects.all()
# 			self.fields['Product_Name'].queryset = Product.objects.filter(Name=self.fields['Company_Name']).values()

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

class PI_PriceForm(forms.ModelForm):
	class Meta:
		model = PI_Purchase_Price
		fields = [
			'Invoice_Id',
			'Final_Amount',
			'Additions',
			'Deductions',
			'Revised_Amount',
			'Comments'
		]
		widgets = {
			'Invoice_Id': forms.TextInput(attrs={'class': 'form-control'}),
			'Final_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Additions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Deductions': forms.NumberInput(attrs={'class': 'form-control'}),
			'Revised_Amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'Comments': forms.Textarea(attrs={'class':'form-control','placeholder':"Leave a comment here" ,'style':"height: 100px"})
		}
		labels = {
			'Invoice_Id': 'Invoice Id',
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