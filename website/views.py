from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render , redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from .forms import SignUpForm, AddRecordForm, AddProductForm,AddPriceForm,AddPriceForm,AddSymptomForm,AddCompanyForm,PI_ProductForm,PI_InvoiceForm,PI_PriceForm,PI_ProductUpdateForm
# ,AddPruchaseInvoiceForm
from django.core.cache import cache
import json
from .models import Record,Product,Price,symptom,Company,PI_Product_info,PI_Invoice_info,PI_Purchase_Price
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
			return redirect('home')
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
			print(product)
		return render(request, 'product.html', {'product':product})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def product_record(request,pk):
	if request.user.is_authenticated:
		product_record = Product.objects.get(Name=pk)
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
				add_record = form.save()
				messages.success(request, f"{add_record.Name}'s {' Record has been Added!'} ")
				return redirect('product_master')
		return render(request, 'product_add.html', {'form':form})
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


# def product_add(request):
#     form = AddProductForm(request.POST or None)
#     if request.user.is_authenticated:
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             term = request.GET.get('term', '')
#             companies = Company.objects.filter(Company_name__icontains=term)
#             response_content = [{'id': company.Company_name, 'text': company.Company_name} for company in companies]
#             return JsonResponse(response_content, safe=False)
#         if request.method == 'POST':
#             if form.is_valid():
#                 add_record = form.save()
#                 messages.success(request, f"{add_record.Name}'s Record has been Added!")
#                 return redirect('product_master')
#         return render(request, 'product_add.html', {'form': form})
#     else:
#         messages.success(request, 'You must be logged in!')
#         return redirect('home')

# views.py
# views.py
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
			price = Price.objects.filter(ID__icontains = price_q)
		else:
			price = Price.objects.all()
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
	
def price_record(request,pk):
	if request.user.is_authenticated:
		price_rec_var = Price.objects.get(Product=pk)
		return render(request, 'price_record.html', {'price_rec_var':price_rec_var})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def price_update(request, pk):
    if request.user.is_authenticated:
        current_record = get_object_or_404(Price, Product=pk)
        form = AddPriceForm(request.POST or None, instance=current_record)
        
        if form.is_valid():
            update_record = form.save()
            messages.success(request, f"{update_record.Product} Record has been Updated!")
            return redirect('price')
        
        return render(request, 'price_update.html', {'form': form})
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
	
# def load_companies(request):
# 	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
# 		term = request.GET.get('term', '')
# 		companies = Company.objects.filter(Company_name__icontains=term)
# 		response_content = list(companies.values('Company_name'))
# 		print(response_content)
# 		return JsonResponse(response_content, safe=False)
# 	return JsonResponse({'error': 'Invalid request'}, status=400)
	
#Purchase Invoice
def purchase_invoice_home(request):
	if request.user.is_authenticated:
		if 'purchase_invoice_q' in request.GET:
			q =request.GET['purchase_invoice_q']
			records = PI_Invoice_info.objects.filter(Invoice_Id__icontains = q)
		else:
			records = PI_Invoice_info.objects.all()
			print(records)
		return render(request, 'purchase_invoice.html', {'records':records})
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

# def purchase_invoice_add(request):
# 	if request.user.is_authenticated:
# 		if request.method == 'POST':
# 			form = AddPruchaseInvoiceForm(request.POST)
# 			if form.is_valid():
# 				form.save()
# 				return redirect('purchase_invoice_add')
# 		else:
# 			form = AddPruchaseInvoiceForm()
# 		return render(request, 'purchase_invoice_add.html', {'form': form})
# 	else:
# 		messages.error(request, 'You must be logged in!')
# 		return redirect('home')


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


def purchase_invoice_add(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			ttl = 3600
			action_type = request.POST.get('action_type', 'add_update')
			update_action = request.POST.get('update_action', '')

			if action_type == 'add_update':
				invoice_form = PI_InvoiceForm(request.POST)
				product_form = PI_ProductForm(request.POST)
				price_form = PI_PriceForm(request.POST)

				if invoice_form.is_valid() and product_form.is_valid():
					invoice_id = invoice_form.cleaned_data['Invoice_Id']

                    # Update or add the invoice data in the cache
					cached_invoice_details = cache.get("invoice_data", [])
					updated_invoice_details = [inv for inv in cached_invoice_details if inv['Invoice_Id'] != invoice_id]
					updated_invoice_details.append(invoice_form.cleaned_data)
					cache.delete('invoice_data')
					cache.set('invoice_data', updated_invoice_details,ttl)

                    # Update or add the product data in the cache
					cached_product_details = cache.get("product_data", [])
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
                                'Invoice_Id': invoice_id,
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
					cache.set('product_data', cached_product_details,ttl)
					invoice_form = PI_InvoiceForm(request.POST)
					product_form = PI_ProductForm()
					price_form = PI_PriceForm(request.POST)
				else:
					print("Form errors:", invoice_form.errors, product_form.errors,price_form.errors)

			elif action_type == 'delete':
				product_id = request.POST.get('product_id')
				print(product_id)
				product_id = int(product_id)
				if product_id:
					cached_product_details = cache.get("product_data", [])
					updated_product_details = [prod for prod in cached_product_details if prod['Id'] != product_id]

                    # Adjust the IDs of remaining products
					for prod in updated_product_details:
						if prod['Id'] > product_id:
							prod['Id'] -= 1

					cache.set('product_data', updated_product_details,ttl)

		invoice_form = PI_InvoiceForm(request.POST)
		product_form = PI_ProductForm()
		price_form = PI_PriceForm()

		cached_invoice_data = cache.get('invoice_data', [])
		cached_product_data = cache.get('product_data', [])
		context = {
            'invoice_form': invoice_form,
            'product_form': product_form,
			'price_form': price_form,
            'Product_cache': cached_product_data,
			'invoice_cache': cached_invoice_data,
        }

		return render(request, 'purchase_invoice_add.html', context)
	else:
		return redirect('home')



def submit_purchase_invoice_cache(request):
	if request.method == 'POST':
		print(request.POST)
		# Retrieve cached data
		cached_invoice_data = cache.get('invoice_data', [])
		cached_product_data = cache.get('product_data', [])
		price_form = PI_PriceForm(request.POST)
		print(price_form)
		invoice_id_var = ''
		for data in cached_invoice_data:
			PI_Invoice_info.objects.create(
				Invoice_Id = data['Invoice_Id'],
				Invoice_Date = data['Invoice_Date'],
				Company_Name = data['Company_Name'],
				Address = data['Address']
			)
			invoice_id_var += data['Invoice_Id'].upper()
			
		invoice_object = PI_Invoice_info.objects.get(Invoice_Id=data['Invoice_Id'])
        # Save data to the database
		for data in cached_product_data:
			if data['Invoice_Id'].upper() == invoice_id_var:
				PI_Product_info.objects.create(
						Invoice_Id= invoice_object,
						Id = data['Id'],
						Product_Name = data['Product_Name'],
						Batch_No = data['Batch_No'].upper(),
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
						Combo_Pk_Id = str(data['Invoice_Id'].upper()) + '_' + str(data['Product_Name'])+ '_' + str(data['Batch_No']) + '_' +str( data['Size']) + '_' + str(data['Unit'])
            	)
			else:
				messages.success(request, "There's an issue with save statement!")
		if price_form.is_valid():
			print('Price form is valid')
			PI_Purchase_Price.objects.create(
				Invoice_Id = invoice_object,
				Final_Amount = price_form.cleaned_data['Final_Amount'],
				Additions = price_form.cleaned_data['Additions'],
				Deductions = price_form.cleaned_data['Deductions'],
				Revised_Amount = price_form.cleaned_data['Revised_Amount'],
				Comments = price_form.cleaned_data['Comments']
			)
		else:
			print(f'price form errors :-->', price_form.errors)
        # Clear the cache
		cache.delete('invoice_data')
		cache.delete('product_data')
    
	return redirect('purchase_invoice')

def purchase_invoice_record(request,pk):
	if request.user.is_authenticated:
		# if 'symptom_q' in request.GET:
		# 	q =request.GET['symptom_q']
		# 	records = symptom.objects.filter(disease_name__icontains = q)
		# else:
		Invoice_records = PI_Invoice_info.objects.get(Invoice_Id = pk)
		Product_records = PI_Product_info.objects.filter(Invoice_Id = pk)
		Price_records = PI_Purchase_Price.objects.get(Invoice_Id = pk)
		context = {'Invoice_records':Invoice_records,
			       'Product_records':Product_records,
				   'Price_records':Price_records}
		return render(request, 'purchase_invoice_record.html', context)
	else:
		messages.success(request, "You must be logged in..to view that page.")
		return redirect('home')

def purchase_invoice_del(request,pk):
	if request.user.is_authenticated:
		PI_Invoice_Del = PI_Invoice_info.objects.get(Invoice_Id = pk)
		PI_Product_Del = PI_Product_info.objects.get(Invoice_Id = pk)
		PI_Purchase_Del = PI_Purchase_Price.objects.get(Invoice_Id = pk)
		PI_Invoice_Del.delete()
		PI_Product_Del.delete()
		PI_Purchase_Del.delete()
		messages.success(request, f"{PI_Invoice_Del.Invoice_Id}'s {' Record has been deleted!'} ")
		return redirect('purchase_invoice')
	else:
		messages.success(request, 'You must be logged in!')
		return redirect('home')

def purchase_invoice_update_refresh(request, pk):
	cache_list = ['invoice_update', 'product_update', 'price_update']
	for i in cache_list:
		cache.delete(i)
	return redirect('purchase_invoice_update', pk=pk)

def purchase_invoice_update(request, pk):
    if request.user.is_authenticated:
        ttl = 3600
        current_invoice_record = cache.get('invoice_update', PI_Invoice_info.objects.filter(Invoice_Id=pk).values()[0])
        current_product_records = list(cache.get('product_update', PI_Product_info.objects.filter(Invoice_Id=pk).values()))
        current_price_record = cache.get('price_update', PI_Purchase_Price.objects.filter(Invoice_Id=pk).values()[0])

        PI_Invoice_form = PI_InvoiceForm(request.POST or None, instance=PI_Invoice_info.objects.get(Invoice_Id=pk))
        PI_product_form = PI_ProductUpdateForm(request.POST or None)
        PI_price_form = PI_PriceForm(request.POST or None, instance=PI_Purchase_Price.objects.get(Invoice_Id=pk))

        cache.set('invoice_update', current_invoice_record)
        cache.set('product_update', current_product_records)
        cache.set('price_update', current_price_record)

        company_name = PI_Invoice_form.initial['Company_Name']

        if request.method == 'POST':
            action_type = request.POST.get('action_type', 'add_update')
            if action_type == 'add_update':
                if PI_Invoice_form.is_valid():
                    cache.set('invoice_update', PI_Invoice_form.cleaned_data, ttl)
                if PI_product_form.is_valid():
                    new_product_data = PI_product_form.cleaned_data
                    cached_product_records = cache.get('product_update', [])
                    updated = False
                    for prod in cached_product_records:
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
                                'PU_Final_Amount': PI_product_form.cleaned_data['PU_Final_Amount']
                            })
                            updated = True
                            break
                    if not updated:
                        next_id = len(cached_product_records) + 1
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
                            'PU_Final_Amount': PI_product_form.cleaned_data['PU_Final_Amount']
                        }
                        cached_product_records.append(new_product_record)
                    cache.set('product_update', cached_product_records, ttl)
                    current_product_records = cache.get('product_update')
                    PI_product_form = PI_ProductUpdateForm()
                    PI_Invoice_form = PI_InvoiceForm(request.POST or None)
                    PI_price_form = PI_PriceForm(request.POST or None)
                if PI_price_form.is_valid():
                    cache.set('price_update', PI_price_form.cleaned_data, ttl)

            elif action_type == 'delete':
                product_id = int(request.POST.get('product_id'))
                if product_id:
                    updated_product_records = [prod for prod in current_product_records if prod['Id'] != product_id]
                    for prod in updated_product_records:
                        if prod['Id'] > product_id:
                            prod['Id'] -= 1
                    cache.set('product_update', updated_product_records, ttl)

            elif action_type == 'update_db':
                print('Update statement activated')
                cached_invoice = cache.get('invoice_update')
                cached_price = cache.get('price_update')
                cached_product = cache.get('product_update')
                print('cached_invoice:', cached_invoice)
                print('cached_price:', cached_price)
                print('cached_product:', cached_product)
                if cached_invoice:
                    PI_Invoice_Del = PI_Invoice_info.objects.get(Invoice_Id=pk)
                    PI_Invoice_Del.delete()
                    PI_Invoice_form = PI_InvoiceForm(request.POST or None) 
                    cache.set('invoice_update', PI_Invoice_form.cleaned_data if PI_Invoice_form.is_valid() else None, ttl)
                    cached_invoice = cache.get('invoice_update')
                    PI_Invoice_info.objects.create(
                        Invoice_Id=cached_invoice['Invoice_Id'],
                        Invoice_Date=cached_invoice['Invoice_Date'],
                        Company_Name=cached_invoice['Company_Name'],
                        Address=cached_invoice['Address']
                    )
                    invoice_object = PI_Invoice_info.objects.get(Invoice_Id=cached_invoice['Invoice_Id'])
                    if cached_product:
                        for data in cached_product:
                            PI_Product_info.objects.create(
                                Invoice_Id=invoice_object,
                                Id=data['Id'],
                                Product_Name=data['Product_Name'],
                                Batch_No=data['Batch_No'].upper(),
                                Manufacture_date=data['Manufacture_date'],
                                Expiry_date=data['Expiry_date'],
                                Size=data['Size'],
                                Unit=data['Unit'],
                                Quantity=data['Quantity'],
                                BT_Rate=data['BT_Rate'],
                                BT_Final_Amount=data['BT_Final_Amount'],
                                CGST=data['CGST'],
                                SGST=data['SGST'],
                                PU_Final_Amount=data['PU_Final_Amount'],
                                Combo_Pk_Id=str(invoice_object) + '_' + str(data['Product_Name']) + '_' + str(data['Batch_No']) + '_' + str(data['Size']) + '_' + str(data['Unit'])
                            )
                    if cached_price:
                        PI_price_form = PI_PriceForm(request.POST, None)
                        cache.set('price_update', PI_price_form.cleaned_data if PI_price_form.is_valid() else None, ttl)
                        cached_price = cache.get('price_update')
                        PI_Purchase_Price.objects.create(
                            Invoice_Id=invoice_object,
                            Final_Amount=cached_price['Final_Amount'],
                            Additions=cached_price['Additions'],
                            Deductions=cached_price['Deductions'],
                            Revised_Amount=cached_price['Revised_Amount'],
                            Comments=cached_price['Comments']
                        )
                    cache.delete('invoice_update')
                    cache.delete('product_update')
                    cache.delete('price_update')
                return redirect('purchase_invoice')

        context = {
            'invoice_form': PI_Invoice_form,
            'product_form': PI_product_form,
            'price_form': PI_price_form,
            'product_record': current_product_records,
            'invoice_record': current_invoice_record,
            'company_name': company_name,
        }
        return render(request, 'purchase_invoice_update.html', context)
    else:
        messages.success(request, 'You must be logged in!')
        return redirect('home')

