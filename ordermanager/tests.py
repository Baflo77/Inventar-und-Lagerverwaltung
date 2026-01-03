#from django.test import TestCase

from django.test import TestCase
from .models import Order, OrderItem
from customermanager.models import Customer
from productmanager.models import Product


class OrderTestCase(TestCase):
    def setUp(self):
        # Test-Daten erstellen
        self.customer = Customer.objects.create(
            firstname="Max",
            lastname="Müller",
            email="max@test.de"
        )
        self.product = Product.objects.create(
            name="Laptop",
            sku="LAP001",
            unit_price=999.99
        )

    def test_order_creation(self):
        order = Order.objects.create(
            customer=self.customer,
            status="OPEN"
        )
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, "OPEN")

    def test_order_item_creation(self):
        order = Order.objects.create(customer=self.customer)
        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2
        )
        self.assertEqual(item.quantity, 2)
