from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.purchase.models import Supplier, PurchaseOrder, PurchaseOrderLine
from apps.sales.models import Product
from decimal import Decimal

class PurchaseTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='purchaser',
            email='purchase@example.com',
            password='testpass123'
        )
        
        # Create test supplier
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='supplier@example.com',
            phone='1234567890',
            address='Test Address'
        )
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Product',
            code='PRD001',
            description='Test Description',
            unit_price=Decimal('80.00'),
            stock_quantity=0
        )

    def test_supplier_creation(self):
        """Test supplier creation"""
        self.assertEqual(self.supplier.name, 'Test Supplier')
        self.assertEqual(self.supplier.email, 'supplier@example.com')

    def test_purchase_order(self):
        """Test purchase order creation and calculation"""
        order = PurchaseOrder.objects.create(
            supplier=self.supplier,
            order_date='2024-01-01',
            status='draft',
            created_by=self.user
        )
        
        # Add order line
        order_line = PurchaseOrderLine.objects.create(
            order=order,
            product=self.product,
            quantity=5,
            unit_price=Decimal('80.00')
        )

        self.assertEqual(order_line.total(), Decimal('400.00'))
        self.assertEqual(order.total_amount(), Decimal('400.00')) 