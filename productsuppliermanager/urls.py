from rest_framework.routers import DefaultRouter
from .views import ProductSupplierViewSet, productsupplier_list_ui, productsupplier_by_product, productsupplier_by_supplier
from django.urls import path

router = DefaultRouter()
router.register("productsupplier", ProductSupplierViewSet, basename="productsupplier")

urlpatterns = [

    path("", productsupplier_list_ui, name="productsupplier_list_ui"),
    path("api/by-product/", productsupplier_by_product, name="productsupplier_by_product"),
    path("api/by-supplier/", productsupplier_by_supplier, name="productsupplier_by_supplier"),
]

urlpatterns += router.urls


