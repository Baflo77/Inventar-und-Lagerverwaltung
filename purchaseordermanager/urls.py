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
from django.urls import path
from . import views

urlpatterns = [
    path("", views.purchaseorder_ui, name="purchaseorder_ui"),
    path("api/", views.purchaseorder_list, name="purchaseorder_list"),
    path("api/<int:id>/", views.purchaseorder_detail, name="purchaseorder_detail"),
    #Wareneingang
    path("<int:id>/receive/", views.purchaseorder_receive_ui, name="purchaseorder_receive_ui"),
    path("api/<int:id>/receive/", views.purchaseorder_receive_api, name="purchaseorder_receive_api"),
    #stornieren
    path("api/<int:id>/cancel/", views.purchaseorder_cancel_api, name="purchaseorder_cancel_api"),
]
