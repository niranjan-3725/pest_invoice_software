from django.urls import path,include
from . import views


urlpatterns = [
    #path('login/', views.login_user,name='login'),
    path('logout/', views.logout_user,name='logout'),
    path('register/', views.register_user,name='register'),
    # Customer URLS
    path('', views.home,name='home'),
    path('record/<int:pk>', views.customer_record,name='record'),
    path('delete_record/<int:pk>', views.delete_record,name='delete_record'),
    path('add_record/', views.add_record,name='add_record'),
    path('update_record/<int:pk>', views.update_record,name='update_record'),
    #Company URLS
    path('company/',views.company,name = 'company'),
    path('company_add/',views.company_add,name='company_add'),
    path('ajax/load-companies/', views.load_companies, name='ajax_load_companies'),
    path('company_update/<str:pk>',views.company_update,name='company_update'),
    # Products URLS
    path('product_master/', views.product_master,name='product_master'),
    path('product_record/<slug:pk>', views.product_record,name='product_record'),
    path('product_del/<slug:pk>', views.product_del,name='product_del'),
    path('product_update/<slug:pk>', views.product_update,name='product_update'),
    path('product_add/', views.product_add,name='product_add'),
    # Price URLS
    path('price/', views.price,name='price'),
    path('price_add/', views.price_add,name='price_add'),
    path('price_record/<slug:pk>/<slug:size>/<slug:unit>/', views.price_record,name='price_record'),
    path('price_update/<slug:pk>/<slug:size>/<slug:unit>/<slug:batch_no>/', views.price_update,name='price_update'),
    path('price_del/<slug:pk>', views.price_del,name='price_del'),
    # Symptom URLS
    path('symptom_page/', views.symptom_page,name='symptom_page'),
    path('symptom_add/', views.symptom_add,name='symptom_add'),
    path('symptom_record/<str:pk>', views.symptom_record,name='symptom_record'),
    path('symptom_del/<str:pk>', views.symptom_del,name='symptom_del'),
    path('symptom_update/<str:pk>', views.symptom_update,name='symptom_update'),

    #Inventory URLS
    path('inventory/',views.Inventory,name= 'inventory'),
    path('inventory_detail/<slug:product>/<int:Size>/<slug:Unit>',views.Inventory_detail,name= 'inventory_detail'),
    #Purchase Invoice URLS
    path('purchase_invoice/',views.purchase_invoice_home,name = 'purchase_invoice'),
    path('purchase_invoice_add/', views.purchase_invoice_add, name='purchase_invoice_add'),
    path('get_company_address/', views.get_company_address, name='get_company_address'),
    path('get_product_name',views.get_product_name,name = 'get_product_name'),
    path('get-profit-percentage/', views.get_profit_percentage, name='get_profit_percentage'),
    # path('purchase_invoice_on_db',views.submit_purchase_invoice_cache, name = 'purchase_invoice_on_db'),
    path('purchase_invoice_record/<slug:pk>',views.purchase_invoice_record,name = 'purchase_invoice_record'),
    path('purchase_invoice_del/<slug:pk>',views.purchase_invoice_del,name='purchase_invoice_del'),
    path('purchase_invoice_update/<slug:pk>',views.purchase_invoice_update,name= 'purchase_invoice_update'),
    path('purchase_invoice_update_refresh/<slug:pk>', views.purchase_invoice_update_refresh, name='purchase_invoice_update_refresh'),

    #Return Invoice Urls
    path('return_invoice/',views.return_invoice_home,name = 'return_invoice'),
    path('return_invoice_add/',views.return_invoice_add,name = 'return_invoice_add'),
    path('check_quantity/', views.check_quantity, name='check_quantity'),
    path('get_before_tax_price/',views.get_before_tax_price,name='get_before_tax_price'),
    path('fetch_sizes_for_batch/',views.fetch_sizes_for_batch,name='fetch_sizes_for_batch'),
    path('get-batch-no/',views.get_batch_nos,name = 'get_batch_nos'),
    path('return_invoice_record/<slug:pk>',views.return_invoice_record,name = 'return_invoice_record'),
    path('return_invoice_update/<slug:pk>',views.return_invoice_update,name= 'return_invoice_update'),
    path('check_quantity_RI_Update/',views.check_quantity_RI_Update,name='check_quantity_RI_Update'),
    path('return_invoice_update_refresh/<slug:pk>', views.return_invoice_update_refresh, name='return_invoice_update_refresh'),
    path('return_invoice_del/<slug:pk>',views.return_invoice_del,name = 'return_invoice_del'),

    #Sales Invoive Urls
    path('sale_invoice/',views.Sales_invoice_home,name = 'Sales_invoice'),
    path('sale_invoice_add/',views.sales_invoice_add,name = 'sales_invoice_add'),
    path('load_phone_no/',views.load_mobile_no,name= 'ajax_load_mobile_no'),
    path('get_customer_details/',views.get_customer_details,name = 'get_customer_details'),
    path('get_product_name_based_on_company/',views.get_product_name_based_on_company,name = 'get_product_name_based_on_company'),
    path('get_batch_details/',views.get_batch_details,name = 'get_batch_details'),
    path('get_retail_price/',views.get_retail_price,name='get_retail_price'),
    path('sale_invoice_record/<slug:pk>',views.sale_invoice_record,name = 'sale_invoice_record'),
    path('get_category/',views.get_category,name='get_category'),
    path('sales_invoice_del/<slug:pk>',views.sales_invoice_del,name='sales_invoice_del'),

    #Sales Invoice Update Urls
    path('sale_invoice_update/<slug:pk>',views.sale_invoice_update,name= 'sale_invoice_update'),

    #Sales Return Invoice Urls
    path('sale_return_invoice/',views.Sales_return_invoice_home,name = 'Sales_Return_invoice'),
    path('sale_return_invoice_add/',views.Sales_return_invoice_add, name = 'sales_return_invoice_add'),
    path('get_sales_records/', views.get_sales_records, name='get_sales_records'),
    path('get_selected_items_details/', views.get_selected_items_details, name='get_selected_items_details'),

    #Sales Return Invoice Record Urls
    path('sale_return_invoice_record/<slug:pk>',views.sale_return_invoice_record,name= 'sale_return_invoice_record'),
    path('sale_return_invoice_del/<slug:pk>',views.sales_return_invoice_del,name = 'sales_return_invoice_del'),
    path('sale_return_invoice_update/<slug:pk>',views.sales_return_invoice_update,name= 'sale_return_invoice_update'),
]
