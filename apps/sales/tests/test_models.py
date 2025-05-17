from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.sales.models import Customer, Product, SalesOrder, SalesOrderLine
from decimal import Decimal

class SalesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='salesperson',
            email='sales@example.com',
            password='testpass123'
        )
        
        # Create test customer
        self.customer = Customer.objects.create(
            name='Test Customer',
            email='customer@example.com',
            phone='1234567890',
            address='Test Address'
        )
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Product',
            code='PRD001',
            description='Test Description',
            unit_price=Decimal('100.00'),
            stock_quantity=50
        )

    def test_customer_creation(self):
        """Test customer creation"""
        self.assertEqual(self.customer.name, 'Test Customer')
        self.assertEqual(self.customer.email, 'customer@example.com')

    def test_product_creation(self):
        """Test product creation"""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.unit_price, Decimal('100.00'))
        self.assertEqual(self.product.stock_quantity, 50)

    def test_sales_order(self):
        """Test sales order creation and calculation"""
        order = SalesOrder.objects.create(
            customer=self.customer,
            order_date='2024-01-01',
            status='draft',
            created_by=self.user
        )
        
        # Add order line
        order_line = SalesOrderLine.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=self.product.unit_price
        )

        self.assertEqual(order_line.total(), Decimal('200.00'))
        self.assertEqual(order.total_amount(), Decimal('200.00')) 