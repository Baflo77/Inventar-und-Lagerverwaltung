from django.urls import path
from . import views

urlpatterns = [
    # Orders
    path('orders/', views.show_all_orders, name='show_all_orders'),
    path('orders/<int:id>/', views.show_order_details, name='show_order_details'),

    # OrderItems
    path('order-items/', views.show_all_order_items, name='show_all_order_items'),
    path('order-items/<int:id>/', views.show_order_item_details, name='show_order_item_details'),

    # UI
    path('ui/', views.ordermanager_ui, name='ordermanager_ui'),
]
