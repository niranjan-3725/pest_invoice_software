from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render , redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q,Sum,F
from django.http import JsonResponse
import datetime
from .forms import *
# ,AddPruchaseInvoiceForm
from django.core.cache import cache
import json
from .models import *
# Create your views here.

def home(request):
	if 'q' in request.GET:
		q =request.GET['q']
		#Filters single column data
		#records = Record.objects.filter(first_name__icontains = q)
		# Q Allows to query multiple columns
		multiple_q = Q(Q(first_name__icontains = q)|Q(last_name__icontains =q)|Q(phone__icontains =q)|Q(city__icontains =q))
		records = Record.objects.filter(multiple_q)
	else:
		records = Record.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			context = {'username': request.user.username.replace('_',' ')}  
			return redirect('home',context)
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})

def logout_user(request):
	logout(request)
	messages.success(request,"You have been logged out succesfully!")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def customer_record(request,pk):
	if request.user.is_authenticated:
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def delete_record(request,pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, f"{delete_it.first_name}'s {' Record has been deleted!'} ")
		return redirect('home')
	else:
		messages.success(request, "You must be logged in to access this page!")
		return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == 'POST':
			if form.is_valid():
				add_record = form.save()
				messages.success(request, f"{add_record.first_name} {add_record.last_name}'s {' Record has been Added!'} ")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')

def update_record(request,pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance= current_record)
		if form.is_valid():
			update_record = form.save()
			messages.success(request, f"{update_record.first_name} {update_record.last_name}'s {' Record has been Updated!'} ")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')
	
def company(request):
	if request.user.is_authenticated:
		company_record = Company.objects.all()
		return render(request, 'company.html', {'company_record':company_record})
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('company')

def company_add(request):
	form = AddCompanyForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == 'POST':
			if form.is_valid():
				add_record = form.save()
				messages.success(request, f"{add_record.Company_name}'s {' Record has been Added!'} ")
				return redirect('company')
		return render(request, 'company_add.html', {'form':form})
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('company')

def company_update(request,pk):
	if request.user.is_authenticated:
		current_record = Company.objects.get(Company_name=pk)
		form = AddCompanyForm(request.POST or None, instance= current_record)
		if form.is_valid():
			update_record = form.save()
			messages.success(request, f"{update_record.Company_name}'s {' Record has been Updated!'} ")
			return redirect('company')
		return render(request, 'company_update.html', {'form':form})
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')


def product_master(request):
	if request.user.is_authenticated:
		if 'product_q' in request.GET:
			product_q =request.GET['product_q']
			product = Product.objects.filter(Name__icontains = product_q)
		else:
			product = Product.objects.all()
			print(f'Products--->',product)
		return render(request, 'product.html', {'product':product})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def product_record(request,pk):
	if request.user.is_authenticated:
		product_record = Product.objects.get(Name=pk)
		print(product_record)
		return render(request, 'product_record.html', {'product_record':product_record})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')
	
def product_del(request,pk):
	if request.user.is_authenticated:
		product_del = Product.objects.get(Name = pk)
		product_del.delete()
		messages.success(request, f"{product_del.Name}'s {' Record has been deleted!'} ")
		return redirect('product_master')
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')
	
def product_add(request):
	form = AddProductForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == 'POST':
			if form.is_valid():
				# add_record = form.save()
				# data = form.
				Product.objects.create(
					Name = form.cleaned_data['Name'].upper(),
					Description = form.cleaned_data['Description'],
					hsn_code = form.cleaned_data['hsn_code'],
					Category = form.cleaned_data['Category'],
					Manufacturer = form.cleaned_data['Manufacturer'],
					Formula = form.cleaned_data['Formula'].upper()
				)
				messages.success(request, f"{form.cleaned_data['Name'].upper()}'s {' Record has been Added!'} ")
				return redirect('product_master')
			else:
				print(form.errors)
		return render(request, 'product_add.html',{'form':form})
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')

def load_companies(request):
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		term = request.GET.get('term', '')
		companies = Company.objects.filter(Company_name__icontains=term)
		print(companies)
		response_content = list(companies.values('Company_name'))
		return JsonResponse(response_content, safe=False)
	return JsonResponse({'error': 'Invalid request'}, status=400)

def product_update(request, pk):
	if request.user.is_authenticated:
		current_record = Product.objects.get(Name=pk)
		form = AddProductForm(request.POST or None, instance=current_record)
		if form.is_valid():
			update_record = form.save()
			messages.success(request, f"{update_record.Name}'s {' Record has been Updated!'} ")
			return redirect('product_master')
		return render(request, 'product_update.html', {'form': form})
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')



def price(request):
	if request.user.is_authenticated:
		if 'price_q' in request.GET:
			price_q =request.GET['price_q']
			price = Price.objects.filter(ID__icontains = price_q).values('Product','Size','Unit').distinct()
		else:
			price = Price.objects.values('Product','Size','Unit').distinct()
		return render(request, 'price.html', {'price':price})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def price_add(request):
	form = AddPriceForm(request.POST or None)
	if request.user.is_authenticated:
		if request.headers.get('x-requested-with') == 'XMLHttpRequest':
			term = (request.GET.get('term'))
			Var = Product.objects.all().filter(Name__icontains = term)
			response_content = list(Var.values())
			return JsonResponse(response_content,safe = False)
		if request.method == 'POST':
			form = AddPriceForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('price')
		return render(request,'price_add.html',{'form':form})
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')
	
def price_record(request,pk,size,unit):
	if request.user.is_authenticated:
		price_rec_var = Price.objects.filter(Product=pk,Size= size,Unit = unit)
		return render(request, 'price_record.html', {'price_rec_var':price_rec_var,
											   		'Product':pk,
													'size':size,
													'unit':unit
													})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def price_update(request, pk,size,unit,batch_no):
    if request.user.is_authenticated:
        current_record = get_object_or_404(Price, Product=pk,Size= size,Unit = unit,Batch_No = batch_no)
        form = AddPriceForm(request.POST or None, instance=current_record)
        
        if form.is_valid():
            update_record = form.save()
            messages.success(request, f"{update_record.Product} Record has been Updated!")
            return redirect('price')
        
        return render(request, 'price_update.html', {'form': form,'Product':pk,'Batch_No': batch_no})
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('home')
	
def price_del(request,pk):
	if request.user.is_authenticated:
		price_del = Price.objects.get(Product = pk)
		price_del.delete()
		messages.success(request, f"{price_del.Product}'s {' Record has been deleted!'} ")
		return redirect('price')
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')
	
def symptom_page(request):
	if request.user.is_authenticated:
		if 'symptom_q' in request.GET:
			q =request.GET['symptom_q']
			records = symptom.objects.filter(disease_name__icontains = q)
		else:
			records = symptom.objects.all()
			
		return render(request, 'symptom.html', {'records':records})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')
 

def symptom_add(request):
	if request.user.is_authenticated:
		if request.headers.get('x-requested-with') == 'XMLHttpRequest':
			term = request.GET.get('term')
			products = Product.objects.filter(Formula__icontains=term).distinct()
			# response_content = [
            #     {'id': product.Formula, 'text': product.Formula} for product in products
            # ]
			response_content = list(products.values('Formula'))
			return JsonResponse(response_content, safe=False)
		if request.method == 'POST':
			form = AddSymptomForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('symptom_page')
		else:
			form = AddSymptomForm()
		return render(request, 'symptom_add.html', {'form': form})
	else:
		messages.error(request, 'You must be logged in!')
		return redirect('home')
	
def symptom_record(request,pk):
	if request.user.is_authenticated:
		symptom_rec_var = symptom.objects.get(disease_name=pk)
		return render(request, 'symptom_record.html', {'symptom_rec_var':symptom_rec_var})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')
	
def symptom_del(request,pk):
	if request.user.is_authenticated:
		symptom_del = symptom.objects.get(disease_name = pk)
		symptom_del.delete()
		messages.success(request, f"{symptom_del.disease_name}'s {' Record has been deleted!'} ")
		return redirect('symptom_page')
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')

def symptom_update(request, pk):
    if request.user.is_authenticated:
        current_record = get_object_or_404(symptom, disease_name=pk)
        form = AddSymptomForm(request.POST or None, instance=current_record)
        
        if form.is_valid():
            update_record = form.save()
            messages.success(request, f"{update_record.disease_name} Record has been Updated!")
            return redirect('price')
        
        return render(request, 'symptom_update.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('home')

#Inventory
def Inventory(request):
	if request.user.is_authenticated:
		if 'inventory_q' in request.GET:
			q =request.GET['inventory_q']
			records = inventory.objects.filter(Product_Name__icontains = q)
		else:
			records = inventory.objects.values('Product_Name','Size','Unit').annotate(Quantity=Sum('Quantity')).order_by('Product_Name','-Quantity')
			# inventory.objects.all().order_by('-Quantity')
			print(records)
		return render(request, 'inventory.html', {'records':records})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def Inventory_detail(request,product,Size,Unit):
	if request.user.is_authenticated:
		records = inventory.objects.filter(Product_Name=product,Size=Size,Unit=Unit)
		return render(request, 'inventory_detail.html', {
			'records':records,
			'Product':product,
			'Size':Size,
			'Unit':Unit
			}
			)
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

#inventory Addition or Updation logic
def Add_Or_Update_to_inventory(product_lst,var,old_dict,Inv_Id):
	existing_combo_ids = inventory.objects.filter(Combo_Id__in=product_lst).values_list('Combo_Id', flat=True)
	old = [item for item in product_lst if item in existing_combo_ids]
	
	new = [item for item in product_lst if item not in existing_combo_ids]
	if var == 'PI':
		for product in new:
			Values  = PI_Product_info.objects.filter(Combo_Id =product , Invoice_Id =Inv_Id).values_list(
				'Product_Name',
				'Batch_No',
				'Size',
				'Unit',
				'Quantity',
				'Manufacture_date',
				'Expiry_date',
				'Combo_Id'
			)
			product_list = [dict(zip(('Product_Name', 'Batch_No', 'Size', 'Unit', 'Quantity', 'Manufacture_date', 'Expiry_date', 'Combo_Id'), item)) for item in Values]
			for data in product_list:
				inventory.objects.create(
					Product_Name = data['Product_Name'],
					Batch_No = data['Batch_No'],
					Size = data['Size'],
					Unit = data['Unit'],
					Quantity = data['Quantity'],
					Manufacture_date = data['Manufacture_date'],
					Expiry_date = data['Expiry_date'],
					Combo_Id = data['Combo_Id']
				)
	# if var == 'PI_Update':
		for product in old:
			Values = PI_Product_info.objects.filter(Combo_Id = product, Invoice_Id =Inv_Id).values_list(
				'Product_Name',
				'Batch_No',
				'Size',
				'Unit',
				'Quantity',
				'Manufacture_date',
				'Expiry_date',
				'Combo_Id'
			)
			New_product_list = [dict(zip(('Product_Name', 'Batch_No', 'Size', 'Unit', 'Quantity', 'Manufacture_date', 'Expiry_date', 'Combo_Id'), item)) for item in Values]
			print(f'Old Dict-->',old_dict)
			print('New Product List --->',New_product_list)
			for i in New_product_list:
				for j in old_dict:
					if i['Combo_Id'] == j['Combo_Id']:
						i['Quantity'] -= j['Quantity']
						#need to make changes here..
					if j['Flag'] == 'Yes':
						inventory.objects.filter(Combo_Id = j['Combo_Id']).update(
							Quantity = j['Quantity']
						)
			print(f'After New Product List -->',New_product_list)
			for data in New_product_list:
				inventory.objects.filter(Combo_Id = data['Combo_Id']).update(
				Product_Name = data['Product_Name'],
				Batch_No = data['Batch_No'],
				Size = data['Size'],
				Unit = data['Unit'],
				Quantity = F('Quantity') + data['Quantity'],
				Manufacture_date = data['Manufacture_date'],
				Expiry_date = data['Expiry_date'],
				Combo_Id = data['Combo_Id']
			)
	if var == 'DEL':
		for data in old_dict:
			inventory.objects.filter(Combo_Id = data['Combo_Id']).update(
				Quantity = F('Quantity') - data['Quantity'],
			)
		
	
#Purchase Invoice
def purchase_invoice_home(request):
	if request.user.is_authenticated:
		if 'purchase_invoice_q' in request.GET:
			q =request.GET['purchase_invoice_q']
			records = PI_Invoice_info.objects.filter(Invoice_Id__icontains = q)
		else:
			records = PI_Invoice_info.objects.all()
			cache.delete('PI_invoice_data')
			cache.delete('PI_product_data')
			# print(records)
		return render(request, 'purchase_invoice.html', {'records':records})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def get_company_address(request):
	if request.user.is_authenticated:
		company_name = request.GET.get('company_name', '')
		try:
			company = Company.objects.get(Company_name=company_name)
			response_content = {'address': company.Address}
		except Company.DoesNotExist:
			response_content = {'error': 'Company not found'}
		return JsonResponse(response_content)
	return JsonResponse({'error': 'Invalid request'}, status=400)

def get_product_name(request):
	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		term = request.GET.get('term', '')
		Products = Product.objects.filter(Name__icontains=term)
		response_content = list(Products.values('Name'))
		return JsonResponse(response_content, safe=False)
	return JsonResponse({'error': 'Invalid request'}, status=400)

def get_profit_percentage(request):
    product_name = request.GET.get('product_name')
    batch_no = request.GET.get('batch_no')
    size = request.GET.get('size')
    unit = request.GET.get('unit')

    try:
        price = Price.objects.get(
            Product=product_name,
            Batch_No=batch_no,
            Size=size,
			Unit = unit
            # Optionally filter by quantity if needed
        )
        data = {
            'profit_percentage': price.Profit_percentage,
        }
    except Price.DoesNotExist:
        data = {
            'profit_percentage': None,
        }

    return JsonResponse(data)

def purchase_invoice_add(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			ttl = 3600
			action_type = request.POST.get('action_type', 'add_update')
			update_action = request.POST.get('update_action', '')

			if action_type == 'add_update':
				PI_invoice_form = PI_InvoiceForm(request.POST)
				PI_product_form = PI_ProductForm(request.POST)
				PI_price_form = PI_PriceForm(request.POST)
				price_form = AddPriceForm(request.POST)

				if PI_invoice_form.is_valid():
					invoice_id = PI_invoice_form.cleaned_data['Invoice_Id']

                    # Update or add the invoice data in the cache
					cached_PI_invoice_details = cache.get("PI_invoice_data", [])
					updated_PI_invoice_details = [inv for inv in cached_PI_invoice_details if inv['Invoice_Id'] != invoice_id]
					updated_PI_invoice_details.append(PI_invoice_form.cleaned_data)
					cache.delete('PI_invoice_data')
					cache.set('PI_invoice_data', updated_PI_invoice_details,ttl)
				if PI_product_form.is_valid() and price_form.is_valid():
                    # Update or add the product data in the cache
					# print('This is true, Cache is updating')
					cached_PI_product_details = cache.get("PI_product_data", [])
					if update_action == 'update':
						product_id = int(request.POST.get('product_id'))
						for prod in cached_PI_product_details:
							if prod['Id'] == product_id:
								prod.update({
                                    'Product_Name': PI_product_form.cleaned_data['Product_Name'],
                                    'Batch_No': PI_product_form.cleaned_data['Batch_No'],
                                    'Manufacture_date': PI_product_form.cleaned_data['Manufacture_date'],
                                    'Expiry_date': PI_product_form.cleaned_data['Expiry_date'],
                                    'Size': PI_product_form.cleaned_data['Size'],
                                    'Unit': PI_product_form.cleaned_data['Unit'],
                                    'Quantity': PI_product_form.cleaned_data['Quantity'],
                                    'BT_Rate': PI_product_form.cleaned_data['BT_Rate'],
                                    'BT_Final_Amount': PI_product_form.cleaned_data['BT_Final_Amount'],
                                    'CGST': PI_product_form.cleaned_data['CGST'],
                                    'SGST': PI_product_form.cleaned_data['SGST'],
                                    'PU_Final_Amount': PI_product_form.cleaned_data['PU_Final_Amount'],
									'MRP':price_form.cleaned_data['MRP'],
									'Cost_Price': price_form.cleaned_data['Cost_Price'],
									'Profit_percentage': price_form.cleaned_data['Profit_percentage'],
									'Selling_Price':price_form.cleaned_data['Selling_Price']
                                })
								break
					else:
						updated = False
						for prod in cached_PI_product_details:
							if (prod['Product_Name'] == PI_product_form.cleaned_data['Product_Name'] 
		   						and prod['Batch_No'] == PI_product_form.cleaned_data['Batch_No'] 
								and prod['Size'] == PI_product_form.cleaned_data['Size'] 
								and prod['Unit'] == PI_product_form.cleaned_data['Unit']
								):
								prod.update({
                                    'Manufacture_date': PI_product_form.cleaned_data['Manufacture_date'],
                                    'Expiry_date': PI_product_form.cleaned_data['Expiry_date'],
                                    'Quantity': PI_product_form.cleaned_data['Quantity'],
                                    'BT_Rate': PI_product_form.cleaned_data['BT_Rate'],
                                    'BT_Final_Amount': PI_product_form.cleaned_data['BT_Final_Amount'],
                                    'CGST': PI_product_form.cleaned_data['CGST'],
                                    'SGST': PI_product_form.cleaned_data['SGST'],
                                    'PU_Final_Amount': PI_product_form.cleaned_data['PU_Final_Amount'],
									'MRP':price_form.cleaned_data['MRP'],
									'Cost_Price': price_form.cleaned_data['Cost_Price'],
									'Profit_percentage': price_form.cleaned_data['Profit_percentage'],
									'Selling_Price':price_form.cleaned_data['Selling_Price']
                                })
								updated = True
								break

						if not updated:
							next_id = len(cached_PI_product_details) + 1
							new_product_record = {
                                'Invoice_Id': invoice_id,
                                'Id': next_id,
                                'Product_Name': PI_product_form.cleaned_data['Product_Name'],
                                'Batch_No': PI_product_form.cleaned_data['Batch_No'],
                                'Manufacture_date': PI_product_form.cleaned_data['Manufacture_date'],
                                'Expiry_date': PI_product_form.cleaned_data['Expiry_date'],
                                'Size': PI_product_form.cleaned_data['Size'],
                                'Unit': PI_product_form.cleaned_data['Unit'],
                                'Quantity': PI_product_form.cleaned_data['Quantity'],
                                'BT_Rate': PI_product_form.cleaned_data['BT_Rate'],
                                'BT_Final_Amount': PI_product_form.cleaned_data['BT_Final_Amount'],
                                'CGST': PI_product_form.cleaned_data['CGST'],
                                'SGST': PI_product_form.cleaned_data['SGST'],
                                'PU_Final_Amount': PI_product_form.cleaned_data['PU_Final_Amount'],
								'MRP':price_form.cleaned_data['MRP'],
								'Cost_Price': price_form.cleaned_data['Cost_Price'],
								'Profit_percentage': price_form.cleaned_data['Profit_percentage'],
								'Selling_Price':price_form.cleaned_data['Selling_Price']
                            }
							cached_PI_product_details.append(new_product_record)
					cache.set('PI_product_data', cached_PI_product_details,ttl)
					PI_invoice_form = PI_InvoiceForm(request.POST)
					PI_product_form = PI_ProductForm()
					price_form = AddPriceForm()
					PI_price_form = PI_PriceForm(request.POST)
				# if PI_price_form.is_valid():
				# 	cache.set('PI_price_data', PI_price_form.cleaned_data, ttl)
				else:
					print("Form errors:", PI_invoice_form.errors, PI_product_form.errors,price_form.errors)

			elif action_type == 'delete':
				product_id = request.POST.get('product_id')
				# print(product_id)
				product_id = int(product_id)
				if product_id:
					cached_PI_product_details = cache.get("PI_product_data", [])
					updated_PI_product_details = [prod for prod in cached_PI_product_details if prod['Id'] != product_id]

                    # Adjust the IDs of remaining products
					for prod in updated_PI_product_details:
						if prod['Id'] > product_id:
							prod['Id'] -= 1

					cache.set('PI_product_data', updated_PI_product_details,ttl)
			elif action_type == 'update_db':
				
				cached_PI_invoice_data = cache.get('PI_invoice_data', [])
				cached_PI_product_data = cache.get('PI_product_data', [])
				cached_PI_price_data = cache.get('PI_price_data', [])
				invoice_id_var = ''
				for data in cached_PI_invoice_data:
					PI_Invoice_info.objects.create(
                        Invoice_Id = data['Invoice_Id'],
                        Invoice_Date = data['Invoice_Date'],
                        Company_Name = data['Company_Name'].upper(),
                        Address = data['Address'].upper()
                            )
					invoice_id_var += data['Invoice_Id'].upper()
                
				invoice_object = PI_Invoice_info.objects.get(Invoice_Id=data['Invoice_Id'])
                # Save data to the database
				products_lst = []
				for data in cached_PI_product_data:
					if not Price.objects.filter(Product=data['Product_Name'].upper(),
												Batch_No = str(data['Batch_No']).upper(),
												Size = data['Size'],
				 								Unit = data['Unit'],
                                				).exists():
						Price.objects.create(
                            Combo_ID = str(data['Product_Name']).upper()+ '_' + str(data['Batch_No']).upper() + '_' +str( data['Size']) + '_' + str(data['Unit']),
                            Product = data['Product_Name'].upper(),
                            Batch_No = str(data['Batch_No']).upper(),
                            Size = data['Size'],
                            Unit = data['Unit'],
                            MRP = data['MRP'],
                            Befor_Tax_price = data['BT_Rate'],
                            Cost_Price = data['Cost_Price'],
                            Profit_percentage = data['Profit_percentage'],
                            Selling_Price = data['Selling_Price']
                        )
					elif Price.objects.filter(Product=data['Product_Name'].upper(),
											Batch_No = str(data['Batch_No']).upper(),
											Size = data['Size'],
				 							Unit = data['Unit'],
                                			).exists():
						Price.objects.update(
                            MRP = data['MRP'],
                            Befor_Tax_price = data['BT_Rate'],
                            Cost_Price = data['Cost_Price'],
                            Profit_percentage = data['Profit_percentage'],
                            Selling_Price = data['Selling_Price']
                            )
					combo_id = str(data['Product_Name']).upper() + '_' + str(data['Batch_No']).upper() + '_' + str(data['Size']) + '_' + str(data['Unit'])
					try:
						price_instance = Price.objects.get(Combo_ID=combo_id)
					except Price.DoesNotExist:
					# Handle the case where no matching Price instance is found
						price_instance = None
					if data['Invoice_Id'].upper() == invoice_id_var:
						PI_Product_info.objects.create(
                            Invoice_Id= invoice_object,
                            Id = data['Id'],
                            Product_Name = data['Product_Name'].upper(),
                            Batch_No = str(data['Batch_No']).upper(),
                            Manufacture_date = data['Manufacture_date'],
                            Expiry_date = data['Expiry_date'],
                            Size = data['Size'],
                            Unit = data['Unit'],
                            Quantity = data['Quantity'],
                            BT_Rate = data['BT_Rate'],
                            BT_Final_Amount = data['BT_Final_Amount'],
                            CGST = data['CGST'],
                            SGST = data['SGST'],
                            PU_Final_Amount = data['PU_Final_Amount'],
                            Combo_Pk_Id = str(data['Invoice_Id'].upper()) + '_' + str(data['Product_Name']).upper()+ '_' + str(data['Batch_No']).upper() + '_' +str( data['Size']) + '_' + str(data['Unit']),
                            Combo_Id = price_instance
                        )
						products_lst.append(str(data['Product_Name']).upper()+ '_' + str(data['Batch_No']).upper() + '_' +str( data['Size']) + '_' + str(data['Unit']))

					else:
						messages.success(request, "There's an issue with save statement!")
				PI_price_form = PI_PriceForm(request.POST)
				if PI_price_form.is_valid():
					PI_Purchase_Price.objects.create(
                        Invoice_Id = invoice_object,
                        Final_Amount = PI_price_form.cleaned_data['Final_Amount'],
                        Additions = PI_price_form.cleaned_data['Additions'],
                        Deductions = PI_price_form.cleaned_data['Deductions'],
                        Revised_Amount = PI_price_form.cleaned_data['Revised_Amount'],
                        Comments = PI_price_form.cleaned_data['Comments']
                        )
				Add_Or_Update_to_inventory(
                    product_lst= products_lst,
                    var='PI',
                    old_dict=[],
                     Inv_Id=invoice_object)
                # Clear the cache
				return redirect('purchase_invoice')

		PI_invoice_form = PI_InvoiceForm(request.POST)
		PI_product_form = PI_ProductForm()
		PI_price_form = PI_PriceForm(request.POST)
		price_form = AddPriceForm()

		cached_PI_invoice_data = cache.get('PI_invoice_data', [])
		cached_PI_product_data = cache.get('PI_product_data', [])
		context = {
            'PI_invoice_form': PI_invoice_form,
            'PI_product_form': PI_product_form,
			'PI_price_form': PI_price_form,
			'price_form': price_form,
            'Product_cache': cached_PI_product_data,
			'invoice_cache': cached_PI_invoice_data,
        }
		return render(request, 'purchase_invoice_add.html', context)
	else:
		return redirect('home')

def purchase_invoice_record(request,pk):
	if request.user.is_authenticated:
		# if 'symptom_q' in request.GET:
		# 	q =request.GET['symptom_q']
		# 	records = symptom.objects.filter(disease_name__icontains = q)
		# else:
		PI_Invoice_records = PI_Invoice_info.objects.get(Invoice_Id = pk)
		PI_Product_records = PI_Product_info.objects.select_related('Combo_Id').filter(Invoice_Id=pk).order_by('Id')
		PI_Price_records = PI_Purchase_Price.objects.get(Invoice_Id = pk)
		context = {'PI_Invoice_records':PI_Invoice_records,
			       'PI_Product_records':PI_Product_records,
				   'PI_Price_records':PI_Price_records}
		return render(request, 'purchase_invoice_record.html', context)
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def purchase_invoice_del(request,pk):
	if request.user.is_authenticated:
		PI_Invoice_Del = PI_Invoice_info.objects.get(Invoice_Id = pk)
		PI_Product_Del = PI_Product_info.objects.filter(Invoice_Id = pk)
		# products_lst = PI_Product_info.objects.filter(Invoice_Id = pk).values_list('Combo_Id')
		old_quant = PI_Product_info.objects.filter(Invoice_Id = pk).values_list('Combo_Id','Quantity')
		old_dict = [dict(zip(('Combo_Id','Quantity'),item)) for item in old_quant]
		PI_Purchase_Del = PI_Purchase_Price.objects.get(Invoice_Id = pk)
		PI_Invoice_Del.delete()
		PI_Product_Del.delete()
		PI_Purchase_Del.delete()
		Add_Or_Update_to_inventory(
			product_lst= [],
			var='DEL',
			old_dict=old_dict,
			Inv_Id=pk)
		messages.success(request, f"{pk}'s {' Record has been deleted!'} ")
		return redirect('purchase_invoice')
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')

def purchase_invoice_update_refresh(request, pk):
	cache_list = ['PI_invoice_update', 'PI_product_update', 'PI_price_update']
	for i in cache_list:
		cache.delete(i)
	return redirect('purchase_invoice_update', pk=pk)


##Need to work on this...
def purchase_invoice_update(request, pk):
	if request.user.is_authenticated:
		ttl = 3600
		current_PI_invoice_record = cache.get('PI_invoice_update', PI_Invoice_info.objects.filter(Invoice_Id=pk).values()[0])
		# current_PI_product_records = list(cache.get('PI_product_update', PI_Product_info.objects.filter(Invoice_Id=pk).values()))
		product_data = PI_Product_info.objects.select_related('Combo_Id').filter(Invoice_Id=pk).order_by('Id')
		product_var_list = []
		for data in product_data:
			product_var_list.append(
				{'Invoice_Id':data.Invoice_Id,
	 			'Id':data.Id,
				'Product_Name':data.Product_Name,
	 			'Batch_No':data.Batch_No,
				'Size':data.Size,
				'Unit':data.Unit,
				'Manufacture_date':data.Manufacture_date,
				'Expiry_date':data.Expiry_date,
				'Quantity':data.Quantity,
				'BT_Rate':data.BT_Rate,
				'BT_Final_Amount':data.BT_Final_Amount,
				'CGST':data.CGST,
				'SGST':data.SGST,
				'PU_Final_Amount':data.PU_Final_Amount,
				'Combo_Pk_Id': data.Combo_Pk_Id,
				'Combo_Id':data.Combo_Id,
				'MRP':data.Combo_Id.MRP,
				'Cost_Price':data.Combo_Id.Cost_Price,
				'Profit_percentage':data.Combo_Id.Profit_percentage,
				'Selling_Price':data.Combo_Id.Selling_Price,
				'Flag': '',
				}
				)
		current_PI_product_records = cache.get('PI_product_update',product_var_list)
		# print('current_PI_product_records---->',current_PI_product_records)
		current_PI_price_record = cache.get('PI_price_update', PI_Purchase_Price.objects.filter(Invoice_Id=pk).values()[0])

		PI_Invoice_form = PI_InvoiceForm(request.POST or None, instance=PI_Invoice_info.objects.get(Invoice_Id=pk))
		PI_product_form = PI_ProductUpdateForm(request.POST or None)
		price_form = AddPriceForm(request.POST or None)
		PI_price_form = PI_PriceForm(request.POST or None, instance=PI_Purchase_Price.objects.get(Invoice_Id=pk))

		cache.set('PI_invoice_update', current_PI_invoice_record)
		cache.set('PI_product_update', current_PI_product_records)
		cache.set('PI_price_update', current_PI_price_record)

		company_name = PI_Invoice_form.initial['Company_Name']

		if request.method == 'POST':
			action_type = request.POST.get('action_type', 'add_update')
			if action_type == 'add_update':
				if PI_Invoice_form.is_valid():
					cache.set('PI_invoice_update', PI_Invoice_form.cleaned_data, ttl)
				if PI_product_form.is_valid() and price_form.is_valid():
					new_product_data = PI_product_form.cleaned_data
					cached_PI_product_records = cache.get('PI_product_update', [])
					updated = False
					for prod in cached_PI_product_records:
						if (prod['Product_Name'] == new_product_data['Product_Name'] and
                            prod['Batch_No'] == new_product_data['Batch_No'] and
                            prod['Size'] == new_product_data['Size'] and
                            prod['Unit'] == new_product_data['Unit']):
							prod.update({
                                'Manufacture_date': PI_product_form.cleaned_data['Manufacture_date'],
                                'Expiry_date': PI_product_form.cleaned_data['Expiry_date'],
                                'Quantity': PI_product_form.cleaned_data['Quantity'],
                                'BT_Rate': PI_product_form.cleaned_data['BT_Rate'],
                                'BT_Final_Amount': PI_product_form.cleaned_data['BT_Final_Amount'],
                                'CGST': PI_product_form.cleaned_data['CGST'],
                                'SGST': PI_product_form.cleaned_data['SGST'],
                                'PU_Final_Amount': PI_product_form.cleaned_data['PU_Final_Amount'],
								'MRP':price_form.cleaned_data['MRP'],
								'Cost_Price': price_form.cleaned_data['Cost_Price'],
								'Profit_percentage': price_form.cleaned_data['Profit_percentage'],
								'Selling_Price':price_form.cleaned_data['Selling_Price'],
								'Flag':'',
                            })
							updated = True
							break
					if not updated:
						next_id = len(cached_PI_product_records) + 1
						new_product_record = {
                            'Invoice_Id': pk,
                            'Id': next_id,
                            'Product_Name': PI_product_form.cleaned_data['Product_Name'],
                            'Batch_No': PI_product_form.cleaned_data['Batch_No'].upper(),
                            'Manufacture_date': PI_product_form.cleaned_data['Manufacture_date'],
                            'Expiry_date': PI_product_form.cleaned_data['Expiry_date'],
                            'Size': PI_product_form.cleaned_data['Size'],
                            'Unit': PI_product_form.cleaned_data['Unit'],
                            'Quantity': PI_product_form.cleaned_data['Quantity'],
                            'BT_Rate': PI_product_form.cleaned_data['BT_Rate'],
                            'BT_Final_Amount': PI_product_form.cleaned_data['BT_Final_Amount'],
                            'CGST': PI_product_form.cleaned_data['CGST'],
                            'SGST': PI_product_form.cleaned_data['SGST'],
                            'PU_Final_Amount': PI_product_form.cleaned_data['PU_Final_Amount'],
							'MRP':price_form.cleaned_data['MRP'],
							'Cost_Price': price_form.cleaned_data['Cost_Price'],
							'Profit_percentage': price_form.cleaned_data['Profit_percentage'],
							'Selling_Price':price_form.cleaned_data['Selling_Price'],
							'Flag':'',
                        }
						cached_PI_product_records.append(new_product_record)
					cache.set('PI_product_update', cached_PI_product_records, ttl)
					current_PI_product_records = cache.get('PI_product_update')
					PI_product_form = PI_ProductUpdateForm()
					price_form = AddPriceForm()
					PI_Invoice_form = PI_InvoiceForm(request.POST or None)
					PI_price_form = PI_PriceForm(request.POST or None)
				if PI_price_form.is_valid():
					cache.set('PI_price_update', PI_price_form.cleaned_data, ttl)

			elif action_type == 'delete':
				product_id = int(request.POST.get('product_id'))
				current_PI_product_records = cache.get('PI_product_update')
				# print(f'product_id --->',product_id)
				if product_id:
					# updated_PI_product_records = [prod for prod in current_PI_product_records if prod['Id'] != product_id]
					# updated_PI_product_records = [{ prod['Id']: {**prod, 'Flag': 'Yes'} if prod['Id'] != product_id else prod
					# 								for prod in current_PI_product_records
					# 							}]
					updated_PI_product_records = []
					print(f'current_PI_product_records before delete --->',current_PI_product_records)
					print(f'product_id --->',product_id)
					for prod in current_PI_product_records:
						if prod['Id'] == product_id:
							prod['Flag'] = 'Yes'
						if prod['Id'] > product_id and prod['Flag'] != 'Yes':
							prod['Id'] -= 1
						updated_PI_product_records.append(prod)
					cache.set('PI_product_update', updated_PI_product_records, ttl)
					print(f'updated_PI_product_records after delete statement--->' ,updated_PI_product_records)
				current_PI_product_records = cache.get('PI_product_update')
				
				PI_product_form = PI_ProductUpdateForm()
				price_form = AddPriceForm()
				PI_Invoice_form = PI_InvoiceForm(request.POST or None)
				PI_price_form = PI_PriceForm(request.POST or None)

			elif action_type == 'update_db':
				cached_PI_invoice = cache.get('PI_invoice_update')
				cached_PI_price = cache.get('PI_price_update')
				cached_PI_product = cache.get('PI_product_update')
				if cached_PI_invoice['Invoice_Id'] == pk:
					old_quant = PI_Product_info.objects.filter(Invoice_Id = pk).values_list('Combo_Id','Quantity')
					old_dict = [dict(zip(('Combo_Id','Quantity'),item)) for item in old_quant]
					for data in cached_PI_product:
						if data['Flag'] == 'Yes':
							for j in old_dict:
								if j['Combo_Id'] == data['Product_Name']+'_'+str(data['Batch_No'])+'_'+str(data['Size'])+'_'+data['Unit']:
									j['Quantity'] = 0
									j['Flag'] = 'Yes'
								else:
									j['Flag'] = ''
						else:
							for j in old_dict:
								j['Flag'] = ''
					print(f'cached_PI_product--->',cached_PI_product)
					print(f'old_dict--->',old_dict)
					# PI_Invoice_Del = PI_Invoice_info.objects.get(Invoice_Id=pk)
					# PI_Invoice_Del.delete()
					# PI_Invoice_form = PI_InvoiceForm(request.POST or None) 
					# cache.set('PI_invoice_update', PI_Invoice_form.cleaned_data if PI_Invoice_form.is_valid() else None, ttl)
					# cached_PI_invoice = cache.get('PI_invoice_update')
					PI_Invoice_info.objects.filter(Invoice_Id = pk).update(
                        Invoice_Date=cached_PI_invoice['Invoice_Date'],
                        Company_Name=cached_PI_invoice['Company_Name'],
                        Address=cached_PI_invoice['Address']
                    )
					invoice_object = PI_Invoice_info.objects.get(Invoice_Id=cached_PI_invoice['Invoice_Id'])
				
				for data in cached_PI_product:
					if not Price.objects.filter(Product=str(data['Product_Name']).upper(),
												Batch_No = str(data['Batch_No']).upper(),
												Size = data['Size'],
				 								Unit = data['Unit'],
                                				).exists() and data['Flag'] != 'Yes':
						Price.objects.create(
                            Combo_ID = str(data['Product_Name']).upper()+ '_' + str(data['Batch_No']).upper() + '_' +str( data['Size']) + '_' + str(data['Unit']),
                            Product = str(data['Product_Name']).upper(),
                            Batch_No = str(data['Batch_No']).upper(),
                            Size = data['Size'],
                            Unit = data['Unit'],
                            MRP = data['MRP'],
                            Befor_Tax_price = data['BT_Rate'],
                            Cost_Price = data['Cost_Price'],
                            Profit_percentage = data['Profit_percentage'],
                            Selling_Price = data['Selling_Price']
                        )
					elif Price.objects.filter(Product= str(data['Product_Name']).upper(),
											Batch_No = str(data['Batch_No']).upper(),
											Size = data['Size'],
				 							Unit = data['Unit'],
                                			).exists() and data['Flag'] != 'Yes':
						Price.objects.filter(Product=str(data['Product_Name']).upper(),
											Batch_No = str(data['Batch_No']).upper(),
											Size = data['Size'],
				 							Unit = data['Unit'],
                                			).update(
                            MRP = data['MRP'],
                            Befor_Tax_price = data['BT_Rate'],
                            Cost_Price = data['Cost_Price'],
                            Profit_percentage = data['Profit_percentage'],
                            Selling_Price = data['Selling_Price']
                            )
				
				products_lst = []
				for data in cached_PI_product:
					combo_id = str(data['Product_Name']).upper() + '_' + str(data['Batch_No']).upper() + '_' + str(data['Size']) + '_' + str(data['Unit'])
					try:
						price_instance = Price.objects.get(Combo_ID=combo_id)
					except Price.DoesNotExist:
					# Handle the case where no matching Price instance is found
						price_instance = None
					if PI_Product_info.objects.filter(Invoice_Id = data['Invoice_Id']
									   ,Product_Name = str(data['Product_Name']).upper()
									   ,Batch_No = str(data['Batch_No']).upper()
									   ,Size = data['Size']
									   ,Unit = data['Unit']
									   ).exists() and data['Flag'] != 'Yes':
						# print(f'{data['Product_Name']}-{data['Batch_No']} Exits, so updaitng it')
						PI_Product_info.objects.filter(
										Invoice_Id =  data['Invoice_Id']
									   ,Product_Name = str(data['Product_Name']).upper()
									   ,Batch_No = str(data['Batch_No']).upper()
									   ,Size = data['Size']
									   ,Unit = data['Unit']).update(
                                Id=data['Id'],
                                Manufacture_date=data['Manufacture_date'],
                                Expiry_date=data['Expiry_date'],
                                Unit=data['Unit'],
                                Quantity=data['Quantity'],
                                BT_Rate=data['BT_Rate'],
                                BT_Final_Amount=data['BT_Final_Amount'],
                                CGST=data['CGST'],
                                SGST=data['SGST'],
                                PU_Final_Amount=data['PU_Final_Amount'],
                                Combo_Pk_Id=str(invoice_object) + '_' + str(data['Product_Name']) + '_' + str(data['Batch_No']) + '_' + str(data['Size']) + '_' + str(data['Unit']),
								Combo_Id = price_instance
                            )
					if not PI_Product_info.objects.filter(Invoice_Id = data['Invoice_Id']
									   ,Product_Name = str(data['Product_Name']).upper()
									   ,Batch_No = str(data['Batch_No']).upper()
									   ,Size = data['Size']
									   ,Unit = data['Unit']
									   ).exists() and data['Flag'] != 'Yes':
						# print(f'{data['Product_Name']}-{data['Batch_No']} Dosent Exits, so creating it')
						PI_Product_info.objects.create(
										   Invoice_Id = invoice_object,
										   Id = data['Id'],
										   Product_Name = str(data['Product_Name']).upper(),
										   Batch_No = str(data['Batch_No']).upper(),
										   Manufacture_date = data['Manufacture_date'],
										   Expiry_date = data['Expiry_date'],
										   Size = data['Size'],
										   Unit = data['Unit'],
										   Quantity = data['Quantity'],
										   BT_Rate = data['BT_Rate'],
										   BT_Final_Amount = data['BT_Final_Amount'],
										   CGST = data['CGST'],
										   SGST = data['SGST'],
										   PU_Final_Amount = data['PU_Final_Amount'],
										   Combo_Pk_Id = str(invoice_object) + '_' + str(data['Product_Name']) + '_' + str(data['Batch_No']) + '_' + str(data['Size']) + '_' + str(data['Unit']),
										   Combo_Id = price_instance
									   )
					#Deletes values which are not in the cache but in the DB.
					if data['Flag'] == 'Yes':
						print('This Delete statement has been activated')
						# print(f'{data['Product_Name']}-{data['Batch_No']} Dosent Exits in cache, so deleting it')

						PI_Product_info.objects.filter(
						Invoice_Id = data['Invoice_Id']
						,Product_Name = str(data['Product_Name']).upper()
						,Batch_No = str(data['Batch_No']).upper()
						,Size = data['Size']
						,Unit = data['Unit']
						).delete()
					products_lst.append(str(data['Product_Name']).upper()+ '_' + str(data['Batch_No']).upper() + '_' +str( data['Size']) + '_' + str(data['Unit']))
				PI_price_form = PI_PriceForm(request.POST, None)
				if PI_price_form.is_valid():
					# PI_price_form = PI_PriceForm(request.POST, None)
					# cache.set('PI_price_update', PI_price_form.cleaned_data if PI_price_form.is_valid() else None, ttl)
					# cached_PI_price = cache.get('PI_price_update')
					PI_Purchase_Price.objects.filter(Invoice_Id = data['Invoice_Id']).update(
                            Invoice_Id=invoice_object,
                            Final_Amount=PI_price_form.cleaned_data['Final_Amount'],
                            Additions=PI_price_form.cleaned_data['Additions'],
                            Deductions=PI_price_form.cleaned_data['Deductions'],
                            Revised_Amount=PI_price_form.cleaned_data['Revised_Amount'],
                            Comments=PI_price_form.cleaned_data['Comments']
                        )
					# new_quant = PI_Product_info.objects.filter(Invoice_Id = pk).values_list('Combo_Id','Quantity')
					''' <--Logic Starts--> Logic for difference b/w data old values and new values!!'''
					# old_dict = {}
					# new_dict = {}

					# for i in old_quant:
					# 	old_dict[i[0]] = i[1]  
					# for i in new_quant:
					# 	new_dict[i[0]] = i[1]
					# diff = {key: new_dict[key] - old_dict[key] for key in old_dict if key in new_dict}
					
					''' <--Logic Ends-->'''
				print(f'products_lst -->',products_lst)
				print(f'old_dict -->',old_dict)
				Add_Or_Update_to_inventory(
								product_lst= products_lst
								,var='PI'
								,old_dict=old_dict
								,Inv_Id=pk
								)
				cache.delete('PI_invoice_update')
				cache.delete('PI_product_update')
				cache.delete('PI_price_update')
				return redirect('purchase_invoice')
		
		context = {
            'PI_invoice_form': PI_Invoice_form,
            'PI_product_form': PI_product_form,
			'price_form': price_form,
            'PI_price_form': PI_price_form,
            'product_record': current_PI_product_records,
            'invoice_record': current_PI_invoice_record,
            'company_name': company_name,
        }
		
		return render(request, 'purchase_invoice_update.html', context)
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')


#Return Invoice Views

def return_invoice_home(request):
	if request.user.is_authenticated:
		if 'return_invoice_q' in request.GET:
			q =request.GET['return_invoice_q']
			records = RI_Invoice_Info.objects.filter(Return_Id__icontains = q)
		else:
			records = RI_Invoice_Info.objects.all()
			print(records)
		return render(request, 'return_invoice.html', {'records':records})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def return_invoice_add(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			ttl = 3600
			action_type = request.POST.get('action_type', 'add_update')
			update_action = request.POST.get('update_action', '')

			if action_type == 'add_update':
				invoice_form = RI_InvoiceForm(request.POST)
				product_form = RI_ProductForm(request.POST)
				price_form = RI_PriceForm(request.POST)

				if invoice_form.is_valid() and product_form.is_valid():
					return_id = invoice_form.cleaned_data['Return_Id']

                    # Update or add the invoice data in the cache
					cached_invoice_details = cache.get("RI_invoice_data", [])
					updated_invoice_details = [inv for inv in cached_invoice_details if inv['Return_Id'] != return_id]
					updated_invoice_details.append(invoice_form.cleaned_data)
					cache.delete('RI_invoice_data')
					cache.set('RI_invoice_data', updated_invoice_details,ttl)

                    # Update or add the product data in the cache
					cached_product_details = cache.get("RI_product_data", [])
					if update_action == 'update':
						product_id = int(request.POST.get('product_id'))
						for prod in cached_product_details:
							if prod['Id'] == product_id:
								prod.update({
                                    'Product_Name': product_form.cleaned_data['Product_Name'],
                                    'Batch_No': product_form.cleaned_data['Batch_No'],
                                    'Manufacture_date': product_form.cleaned_data['Manufacture_date'],
                                    'Expiry_date': product_form.cleaned_data['Expiry_date'],
                                    'Size': product_form.cleaned_data['Size'],
                                    'Unit': product_form.cleaned_data['Unit'],
                                    'Quantity': product_form.cleaned_data['Quantity'],
                                    'BT_Rate': product_form.cleaned_data['BT_Rate'],
                                    'BT_Final_Amount': product_form.cleaned_data['BT_Final_Amount'],
                                    'CGST': product_form.cleaned_data['CGST'],
                                    'SGST': product_form.cleaned_data['SGST'],
                                    'PU_Final_Amount': product_form.cleaned_data['PU_Final_Amount']
                                })
								break
					else:
						updated = False
						for prod in cached_product_details:
							if (prod['Product_Name'] == product_form.cleaned_data['Product_Name'] and
                                prod['Batch_No'] == product_form.cleaned_data['Batch_No'] and
                                prod['Size'] == product_form.cleaned_data['Size'] and
                                prod['Unit'] == product_form.cleaned_data['Unit']):
								prod.update({
                                    'Manufacture_date': product_form.cleaned_data['Manufacture_date'],
                                    'Expiry_date': product_form.cleaned_data['Expiry_date'],
                                    'Quantity': product_form.cleaned_data['Quantity'],
                                    'BT_Rate': product_form.cleaned_data['BT_Rate'],
                                    'BT_Final_Amount': product_form.cleaned_data['BT_Final_Amount'],
                                    'CGST': product_form.cleaned_data['CGST'],
                                    'SGST': product_form.cleaned_data['SGST'],
                                    'PU_Final_Amount': product_form.cleaned_data['PU_Final_Amount']
                                })
								updated = True
								break

						if not updated:
							next_id = len(cached_product_details) + 1
							new_product_record = {
                                'Return_Id': return_id,
                                'Id': next_id,
                                'Product_Name': product_form.cleaned_data['Product_Name'],
                                'Batch_No': product_form.cleaned_data['Batch_No'],
                                'Manufacture_date': product_form.cleaned_data['Manufacture_date'],
                                'Expiry_date': product_form.cleaned_data['Expiry_date'],
                                'Size': product_form.cleaned_data['Size'],
                                'Unit': product_form.cleaned_data['Unit'],
                                'Quantity': product_form.cleaned_data['Quantity'],
                                'BT_Rate': product_form.cleaned_data['BT_Rate'],
                                'BT_Final_Amount': product_form.cleaned_data['BT_Final_Amount'],
                                'CGST': product_form.cleaned_data['CGST'],
                                'SGST': product_form.cleaned_data['SGST'],
                                'PU_Final_Amount': product_form.cleaned_data['PU_Final_Amount']
                            }
							cached_product_details.append(new_product_record)
					cache.set('RI_product_data', cached_product_details,ttl)
					invoice_form = RI_InvoiceForm(request.POST)
					product_form = RI_ProductForm()
					price_form = RI_PriceForm(request.POST)
				else:
					print("Form errors:", invoice_form.errors, product_form.errors,price_form.errors)

			elif action_type == 'delete':
				product_id = request.POST.get('product_id')
				print(product_id)
				product_id = int(product_id)
				if product_id:
					cached_product_details = cache.get("RI_product_data", [])
					updated_product_details = [prod for prod in cached_product_details if prod['Id'] != product_id]

                    # Adjust the IDs of remaining products
					for prod in updated_product_details:
						if prod['Id'] > product_id:
							prod['Id'] -= 1

					cache.set('RI_product_data', updated_product_details,ttl)
		#Ajax Requests
		if request.headers.get('x-requested-with') == 'XMLHttpRequest':
			request_type = request.GET.get('request_type', '')
			print(request_type)

			if request_type == 'company':
				term = request.GET.get('term', '')
				companies = Company.objects.filter(Company_name__icontains=term)
				response_content = list(companies.values('Company_name'))
				return JsonResponse(response_content, safe=False)
        
			elif request_type == 'product':
				term = request.GET.get('term', '')
				company_name = request.GET.get('company_name', '')
				products = Product.objects.filter(Name__icontains=term, Manufacturer__icontains=company_name)
				response_content = list(products.values('Name'))
				return JsonResponse(response_content, safe=False)
			
			elif request_type == 'batch_no':
				term = request.GET.get('term', '')
				product_name = request.GET.get('product_name', '')
				inv = inventory.objects.filter(Product_Name__icontains = product_name , Batch_No__icontains = term)
				response_content = list(inv.values('Batch_No').distinct())
				return JsonResponse(response_content, safe=False)
		elif request.GET.get('request_type', '') == 'batch_details':
			batch_no = request.GET.get('batch_no', '')
			inv = inventory.objects.filter(Batch_No=batch_no).values('Manufacture_date', 'Expiry_date').first()
			size = inventory.objects.filter(Batch_No=batch_no).values('Size','Unit')
			size_lst = [str(i['Size'])+'-' + i['Unit'] for i in size]
			if inv:
				response_content = {
            'Manufacture_date': inv['Manufacture_date'],
            'Expiry_date': inv['Expiry_date'],
			'sizes': size_lst,
        }
			else:
				response_content = {'error': 'Batch not found'}
			return JsonResponse(response_content)
		last_invoice = RI_Invoice_Info.objects.order_by('-Return_Id').first()

		invoice_form = RI_InvoiceForm(initial={
			'Return_Id' : 1 if last_invoice is None else last_invoice+1,
			'From_Company_Name': request.user.username.replace('_',' '),
			'From_Address':request.user.address}
			)
		product_form = RI_ProductForm()
		price_form = RI_PriceForm()

		cached_invoice_data = cache.get('RI_invoice_data', [])
		cached_product_data = cache.get('RI_product_data', [])
		
		context = {
            'invoice_form': invoice_form,
            'product_form': product_form,
			'price_form': price_form,
            'Product_cache': cached_product_data,
			'invoice_cache': cached_invoice_data,
        }
		return render(request, 'return_invoice_add.html', context)
	else:
		return redirect('home')

def check_quantity(request):
	product_name = request.GET.get('product_name', '')
	batch_no = request.GET.get('batch_no', '')
	var = request.GET.get('size').split('-')
	size = int(var[0])
	unit = var[1]
	entered_quantity = int(request.GET.get('quantity', 0))

    # Get the available quantity from the inventory
	print(f'productname-->',product_name,'<--batch_no-->',batch_no,'<--size-->',size,'<--unit-->',unit)
	inv = inventory.objects.filter(Product_Name=product_name, Batch_No=batch_no,Size = size, Unit = unit).first()
	print(f'inv-->',inv)
	if inv:
		available_quantity = inv.Quantity
		if entered_quantity > available_quantity:
			return JsonResponse({'valid': False, 'available_quantity': available_quantity})
		else:
			return JsonResponse({'valid': True})
	else:
		return JsonResponse({'valid': False, 'error': 'Invalid product or batch number'})