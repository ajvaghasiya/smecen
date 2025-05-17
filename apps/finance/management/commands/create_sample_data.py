from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile
from apps.hr_management.models import Employee, Department, Attendance, LeaveRequest
from apps.finance.models import Account, JournalEntry, JournalItem
from apps.sales.models import Customer, Product, SalesOrder, SalesOrderLine
from apps.purchase.models import Supplier, PurchaseOrder, PurchaseOrderLine
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **kwargs):
        # Create users
        User = get_user_model()
        
        # Create manager
        manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='manager123',
            is_staff=True
        )
        
        # Create employee
        employee = User.objects.create_user(
            username='employee',
            email='employee@example.com',
            password='employee123'
        )

        # Create departments
        it_dept = Department.objects.create(
            name='IT',
            description='Information Technology Department'
        )
        
        hr_dept = Department.objects.create(
            name='HR',
            description='Human Resources Department'
        )

        # Create employees
        emp1 = Employee.objects.create(
            user=employee,
            department=it_dept,
            employee_id='EMP001',
            position='Software Developer',
            salary=Decimal('50000.00')
        )

        # Create attendance records
        today = timezone.now().date()
        for i in range(5):
            Attendance.objects.create(
                employee=emp1,
                date=today - timedelta(days=i),
                status='present'
            )

        # Create leave request
        LeaveRequest.objects.create(
            employee=emp1,
            start_date=today + timedelta(days=10),
            end_date=today + timedelta(days=12),
            leave_type='annual',
            status='pending'
        )

        # Create financial accounts
        cash = Account.objects.create(
            name='Cash',
            code='1000',
            type='asset',
            balance=Decimal('100000.00')
        )
        
        bank = Account.objects.create(
            name='Bank',
            code='1001',
            type='asset',
            balance=Decimal('500000.00')
        )
        
        receivables = Account.objects.create(
            name='Accounts Receivable',
            code='1100',
            type='asset',
            balance=Decimal('0.00')
        )
        
        payables = Account.objects.create(
            name='Accounts Payable',
            code='2000',
            type='liability',
            balance=Decimal('0.00')
        )

        # Create customers
        customer = Customer.objects.create(
            name='ABC Company',
            email='abc@example.com',
            phone='1234567890',
            address='123 Business St'
        )

        # Create products
        laptop = Product.objects.create(
            name='Laptop',
            code='LAP001',
            description='High-end Laptop',
            unit_price=Decimal('1200.00'),
            stock_quantity=10
        )
        
        desktop = Product.objects.create(
            name='Desktop',
            code='DSK001',
            description='Desktop Computer',
            unit_price=Decimal('800.00'),
            stock_quantity=15
        )

        # Create sales order
        sale_order = SalesOrder.objects.create(
            customer=customer,
            order_date=today,
            status='confirmed',
            created_by=manager
        )
        
        SalesOrderLine.objects.create(
            order=sale_order,
            product=laptop,
            quantity=2,
            unit_price=laptop.unit_price
        )

        # Create supplier
        supplier = Supplier.objects.create(
            name='Tech Supplies Ltd',
            email='tech@example.com',
            phone='9876543210',
            address='456 Supply St'
        )

        # Create purchase order
        purchase_order = PurchaseOrder.objects.create(
            supplier=supplier,
            order_date=today,
            status='confirmed',
            created_by=manager
        )
        
        PurchaseOrderLine.objects.create(
            order=purchase_order,
            product=laptop,
            quantity=5,
            unit_price=Decimal('1000.00')
        )

        # Create journal entries
        # Example: Record salary payment
        salary_entry = JournalEntry.objects.create(
            date=today,
            reference='SAL001',
            description='Salary Payment',
            created_by=manager
        )
        
        JournalItem.objects.create(
            entry=salary_entry,
            account=cash,
            debit=Decimal('0.00'),
            credit=Decimal('50000.00')
        )
        
        JournalItem.objects.create(
            entry=salary_entry,
            account=payables,
            debit=Decimal('50000.00'),
            credit=Decimal('0.00')
        )

        self.stdout.write(self.style.SUCCESS('Successfully created sample data')) 