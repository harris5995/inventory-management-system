from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('inventory_product_list/', views.inventory_product_list, name='inventory_product_list'),
    path('inventory_product/<int:pk>', views.inventory_product_detail, name='inventory_product_detail'),
    path('add_inventory_product/', views.add_inventory_product, name='add_inventory_product'), 
    path('csv_upload/', views.csv_upload, name='csv_upload'),
    path('update_inventory_product/<int:pk>', views.update_inventory_product, name='update_inventory_product'),
    path('delete_inventory_product/<int:pk>', views.delete_inventory_product, name='delete_inventory_product'),  

    path('inbound_product_list/', views.inbound_product_list, name='inbound_product_list'),
    path('inbound_product/<int:pk>', views.inbound_product_detail, name='inbound_product_detail'),
    path('add_inbound_product/', views.add_inbound_product, name='add_inbound_product'),
#   path('inbound_csv_upload/', views.inbound_csv_upload, name='inbound_csv_upload'),
    # path('update_inbound_product/', views.update_inbound_product, name='update_inbound_product'),
    # path('delete_inbound_product/', views.delete_inbound_product, name='delete_inbound_product'),

    path('outbound_product_list/', views.outbound_product_list, name='outbound_product_list'),
    # path('outbound_product/<int:pk>', views.outbound_product_detail, name='outbound_product_detail'),
    # path('add_outbound_product/', views.add_outbound_product, name='add_outbound_product'),
    # path('outbound_csv_upload/', views.outbound_csv_upload, name='outbound_csv_upload'),   
    # path('update_outbound_product/', views.update_product_list, name='update_outbound_product'),
    # path('delete_utbound_product/', views.delete_product_list, name='delete_outbound_product'),

]
