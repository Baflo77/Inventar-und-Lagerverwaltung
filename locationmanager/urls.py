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
    # 1. Die HTML Seite (ruft man im Browser auf)
    # URL: /locations/
    path('', views.show_locations, name='show_locations'),

    # 2. Die API für die Daten (nutzt das JavaScript im Hintergrund)
    # URL: /locations/api/list/
    path('api/list/', views.get_locations, name='get_locations'),

    # 3. Die API zum Speichern
    # URL: /locations/api/create/
    path('api/create/', views.write_location, name='write_location'),
]