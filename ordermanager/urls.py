
from django.urls import path
from . import views

urlpatterns = [
    # Orders
    path('', views.show_all_orders, name='show_all_orders'),
    path('<int:id>/', views.show_order_details, name='show_order_details'),

    # OrderItems
    path('items/', views.show_all_order_items, name='show_all_order_items'),
    path('items/<int:id>/', views.show_order_item_details, name='show_order_item_details'),

    # UI
    path('ui/', views.ordermanager_ui, name='ordermanager_ui'),
]
