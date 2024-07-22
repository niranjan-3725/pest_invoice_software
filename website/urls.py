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
    path('product_update/<str:pk>', views.product_update,name='product_update'),
    path('product_add/', views.product_add,name='product_add'),
    # Price URLS
    path('price/', views.price,name='price'),
    path('price_add/', views.price_add,name='price_add'),
    path('price_record/<str:pk>', views.price_record,name='price_record'),
    path('price_update/<str:pk>', views.price_update,name='price_update'),
    path('price_del/<slug:pk>', views.price_del,name='price_del'),
    # Symptom URLS
    path('symptom_page/', views.symptom_page,name='symptom_page'),
    path('symptom_add/', views.symptom_add,name='symptom_add'),
    path('symptom_record/<str:pk>', views.symptom_record,name='symptom_record'),
    path('symptom_del/<str:pk>', views.symptom_del,name='symptom_del'),
    path('symptom_update/<str:pk>', views.symptom_update,name='symptom_update'),
    #Invoice URLS
    path('purchase_invoice/',views.purchase_invoice_home,name = 'purchase_invoice'),
    path('purchase_invoice_add/', views.purchase_invoice_add, name='purchase_invoice_add'),
    path('get_company_address/', views.get_company_address, name='get_company_address'),
    path('get_product_name',views.get_product_name,name = 'get_product_name'),
    path('purchase_invoice_on_db',views.submit_purchase_invoice_cache, name = 'purchase_invoice_on_db'),
    path('purchase_invoice_record/<slug:pk>',views.purchase_invoice_record,name = 'purchase_invoice_record'),
    path('purchase_invoice_del/<slug:pk>',views.purchase_invoice_del,name='purchase_invoice_del'),
    path('purchase_invoice_update/<slug:pk>',views.purchase_invoice_update,name= 'purchase_invoice_update'),
    # path('purchase_invoice_update_refresh/<slug:pk>',views.purchase_invoice_update_refresh,name='purchase_invoice_update_refresh'),
    # path('delete-product/', views.delete_product, name='delete_product'),
    # path('get_cached_products/<str:invoice_id>/', views.get_cached_products, name='get_cached_products'),
    # path('edit_product/<str:invoice_id>/<int:product_index>/', views.edit_product, name='edit_product'),
]
