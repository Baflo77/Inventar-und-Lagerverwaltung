from rest_framework.routers import DefaultRouter
from .views import ProductSupplierViewSet, productsupplier_list_ui
from django.urls import path

router = DefaultRouter()
router.register("productsupplier", ProductSupplierViewSet, basename="productsupplier")

urlpatterns = [

    path("", productsupplier_list_ui, name="productsupplier_list_ui"),
]


urlpatterns += router.urls


