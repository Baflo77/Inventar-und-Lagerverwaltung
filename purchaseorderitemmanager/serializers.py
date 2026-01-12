from rest_framework import serializers
from .models import PurchaseOrderItem
from purchaseordermanager.models import PurchaseOrder
from productsuppliermanager.models import ProductSupplier


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product_supplier.product.name", read_only=True)
    supplier_name = serializers.CharField(source="product_supplier.supplier.name", read_only=True)

    purchase_order_id = serializers.IntegerField(source="purchase_order.id", read_only=True)
    purchase_order_status = serializers.CharField(source="purchase_order.status", read_only=True)
    purchase_order_supplier_name = serializers.CharField(source="purchase_order.supplier.name", read_only=True)

    open_quantity = serializers.SerializerMethodField()
    canceled_quantity = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrderItem
        fields = "__all__"
        extra_kwargs = {
            "received_quantity": {"required": False},
            "line_no": {"required": False},
        }

    def validate(self, data):
        purchase_order = data.get("purchase_order") or getattr(self.instance, "purchase_order", None)
        product_supplier = data.get("product_supplier") or getattr(self.instance, "product_supplier", None)

        if purchase_order and product_supplier:
            if purchase_order.supplier_id != product_supplier.supplier_id:
                raise serializers.ValidationError(
                    {"product_supplier": "Diese Zuordnung gehört nicht zum Lieferanten der PurchaseOrder."}
                )

        return data

    def get_open_quantity(self, obj):
        qty = obj.quantity or 0
        rec = obj.received_quantity or 0
        status = (obj.purchase_order.status or "").lower()

        if status == "canceled":
            return 0
        return max(0, qty - rec)

    def get_canceled_quantity(self, obj):
        qty = obj.quantity or 0
        rec = obj.received_quantity or 0
        status = (obj.purchase_order.status or "").lower()

        if status == "canceled":
            return max(0, qty - rec)
        return 0

