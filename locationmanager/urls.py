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
from locationmanager import views
from django.urls import include
from locationmanager import views

urlpatterns = [
    path("", views.location_list_ui, name="location_list_ui"),
    path("api/", views.show_all_locations, name="location_api_list_create"),
    path("api/<int:id>/", views.location_detail, name="location_api_detail"),
    #path("<int:pk>/edit/", views.location_edit_ui, name="location_edit_ui"),
    path("<int:pk>/delete/", views.location_delete_ui, name="location_delete_ui"),
]