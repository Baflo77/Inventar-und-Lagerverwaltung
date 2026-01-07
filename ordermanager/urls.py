from django.urls import path
from . import views

urlpatterns = [

    path('api/', views.show_all_orders),
    path('api/<int:id>/', views.show_order_details),
    path('api/items/', views.show_all_order_items),
    path('api/items/<int:id>/', views.show_order_item_details),

    path('', views.ordermanager_ui, name='ordermanager_ui'),
]
