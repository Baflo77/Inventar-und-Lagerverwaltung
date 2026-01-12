"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stockmanager import views

from django.urls import include
from stockmanager import views

urlpatterns = [

    path('', views.stock_manager_view, name='stock_manager'),

    path('api/<int:stock_id>/book-out/', views.book_out_api, name='api_book_out'),

    path('api/<int:stock_id>/transfer/', views.transfer_stock_api, name='api_transfer_stock'),

    path('api/delete/<int:stock_id>/', views.delete_stock_api, name='delete_stock_api'),
]
