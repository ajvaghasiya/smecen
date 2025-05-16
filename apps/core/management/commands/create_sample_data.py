from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.hr_management.models import Employee, LeaveRequest, Attendance, Document
from apps.finance.models import (
    Account, JournalEntry, JournalItem, BankAccount, BankReconciliation,
    Transaction, TransactionLine, ExpenseClaim, ExpenseClaimLine, FinancialReport
)
from apps.sales.models import Customer, SalesOrder, Invoice, Payment
from apps.purchase.models import Supplier, PurchaseOrder, Bill
from decimal import Decimal
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample data for demonstration'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cleaning up existing data...')
        
        # Clean up existing data in reverse order to handle dependencies
        ExpenseClaimLine.objects.all().delete()
        ExpenseClaim.objects.all().delete()
        TransactionLine.objects.all().delete()
        Transaction.objects.all().delete()
        BankReconciliation.objects.all().delete()
        BankAccount.objects.all().delete()
        JournalItem.objects.all().delete()
        JournalEntry.objects.all().delete()
        Bill.objects.all().delete()
        PurchaseOrder.objects.all().delete()
        Supplier.objects.all().delete()
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        SalesOrder.objects.all().delete()
        Customer.objects.all().delete()
        Account.objects.all().delete()
        LeaveRequest.objects.all().delete()
        Attendance.objects.all().delete()
        Employee.objects.all().delete()
        # Don't delete the superuser
        User.objects.exclude(username='user').delete()

        self.stdout.write('Creating sample data...')

        # Create users with different roles
        users_data = {
            'admin': {'email': 'admin@example.com', 'password': 'admin123', 'role': 'admin', 'is_staff': True, 'is_superuser': True},
            'hr_manager': {'email': 'hr@example.com', 'password': 'hr123', 'role': 'hr'},
            'accountant': {'email': 'accountant@example.com', 'password': 'accountant123', 'role': 'accountant'},
            'sales_manager': {'email': 'sales@example.com', 'password': 'sales123', 'role': 'manager'},
            'purchase_manager': {'email': 'purchase@example.com', 'password': 'purchase123', 'role': 'manager'},
        }

        created_users = {}
        for username, data in users_data.items():
            user = User.objects.create_user(
                username=username,
                email=data['email'],
                password=data['password'],
                is_staff=data.get('is_staff', False),
                is_superuser=data.get('is_superuser', False)
            )
            user.role = data['role']
            user.phone_number = f'+1555{random.randint(1000000, 9999999)}'
            user.save()
            created_users[username] = user

        # Create additional regular users for employees
        employee_users = []
        for i in range(10):
            username = f'employee{i+1}'
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='employee123',
                role='employee'
            )
            user.phone_number = f'+1555{random.randint(1000000, 9999999)}'
            user.save()
            employee_users.append(user)

        # Create employees with dedicated users
        departments = ['IT', 'HR', 'Finance', 'Sales', 'Operations']
        for i, user in enumerate(employee_users):
            emp = Employee.objects.create(
                user=user,  # Each employee gets their own dedicated user
                employee_id=f'EMP{i+1:03d}',
                department=random.choice(departments),
                position=f'Position {i+1}',
                joining_date=timezone.now() - timedelta(days=random.randint(1, 365)),
                salary=Decimal(random.randint(30000, 100000))
            )

            # Create attendance records with proper timezone awareness
            # Generate a list of unique random dates for each employee
            used_dates = set()
            for _ in range(5):
                while True:
                    date = (timezone.now() - timedelta(days=random.randint(1, 30))).date()
                    if date not in used_dates:
                        used_dates.add(date)
                        break
                
                check_in_time = timezone.make_aware(datetime.combine(date, datetime.min.time().replace(hour=9)))
                check_out_time = timezone.make_aware(datetime.combine(date, datetime.min.time().replace(hour=17)))
                
                Attendance.objects.create(
                    employee=emp,
                    date=date,
                    check_in=check_in_time,
                    check_out=check_out_time,
                    status='present'
                )

            # Create leave requests
            LeaveRequest.objects.create(
                employee=emp,
                start_date=timezone.now() + timedelta(days=random.randint(1, 30)),
                end_date=timezone.now() + timedelta(days=random.randint(31, 60)),
                leave_type='Annual',
                reason='Vacation',
                status=random.choice(['Pending', 'Approved', 'Rejected'])
            )

        # Create financial data
        account_types = ['Asset', 'Liability', 'Income', 'Expense', 'Equity']
        created_accounts = []
        for i in range(10):
            account = Account.objects.create(
                code=f'AC{i+1:03d}',
                name=f'Account {i+1}',
                type=random.choice(account_types),
                balance=Decimal(random.randint(1000, 100000))
            )
            created_accounts.append(account)

        # Create bank accounts
        bank_names = ['Bank of America', 'Chase', 'Wells Fargo', 'Citibank']
        created_bank_accounts = []
        for i in range(4):
            bank_account = BankAccount.objects.create(
                name=f'Main Account {i+1}',
                bank_name=bank_names[i],
                account_number=f'BA{i+1:06d}',
                balance=Decimal(random.randint(10000, 100000))
            )
            created_bank_accounts.append(bank_account)

            # Create bank reconciliations
            BankReconciliation.objects.create(
                bank_account=bank_account,
                statement_date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                statement_balance=bank_account.balance + Decimal(random.randint(-1000, 1000)),
                reconciled_balance=bank_account.balance,
                is_reconciled=random.choice([True, False]),
                reconciled_by=created_users['accountant']
            )

        # Create journal entries and items
        for i in range(5):
            entry = JournalEntry.objects.create(
                date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                reference=f'JE{i+1:04d}',
                description=f'Journal Entry {i+1}',
                created_by=created_users['accountant']
            )

            # Create debit and credit entries
            amount = Decimal(random.randint(1000, 10000))
            JournalItem.objects.create(
                journal_entry=entry,
                account=random.choice(created_accounts),
                debit=amount,
                credit=0
            )
            JournalItem.objects.create(
                journal_entry=entry,
                account=random.choice(created_accounts),
                debit=0,
                credit=amount
            )

        # Create transactions
        transaction_types = ['journal', 'payment', 'receipt', 'transfer']
        for i in range(5):
            transaction = Transaction.objects.create(
                reference_number=f'TR{i+1:04d}',
                transaction_type=random.choice(transaction_types),
                date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                description=f'Transaction {i+1}',
                created_by=created_users['accountant']
            )

            # Create transaction lines
            amount = Decimal(random.randint(1000, 10000))
            TransactionLine.objects.create(
                transaction=transaction,
                account=random.choice(created_accounts),
                description=f'Debit entry for transaction {i+1}',
                debit=amount,
                credit=0
            )
            TransactionLine.objects.create(
                transaction=transaction,
                account=random.choice(created_accounts),
                description=f'Credit entry for transaction {i+1}',
                debit=0,
                credit=amount
            )

        # Create expense claims
        for emp in Employee.objects.all()[:5]:  # Create claims for first 5 employees
            claim = ExpenseClaim.objects.create(
                employee=emp,
                claim_number=f'EXP{emp.id:03d}',
                date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                description='Travel and accommodation expenses',
                total_amount=Decimal(0),  # Will be updated after adding lines
                status=random.choice(['draft', 'submitted', 'approved', 'rejected', 'paid'])
            )

            # Create expense claim lines
            total_amount = Decimal(0)
            categories = ['Travel', 'Accommodation', 'Meals', 'Office Supplies']
            for _ in range(3):
                amount = Decimal(random.randint(100, 1000))
                ExpenseClaimLine.objects.create(
                    claim=claim,
                    expense_date=claim.date - timedelta(days=random.randint(1, 5)),
                    category=random.choice(categories),
                    description=f'Expense for {claim.employee.user.username}',
                    amount=amount
                )
                total_amount += amount

            # Update the total amount
            claim.total_amount = total_amount
            claim.save()

        # Create customers and sales data
        for i in range(5):
            customer = Customer.objects.create(
                name=f'Customer {i+1}',
                email=f'customer{i+1}@example.com',
                phone=f'+1555{random.randint(1000000, 9999999)}',
                address=f'Customer {i+1} Address'
            )
            
            order = SalesOrder.objects.create(
                customer=customer,
                order_number=f'SO{i+1:03d}',
                order_date=timezone.now(),
                total_amount=Decimal(random.randint(1000, 10000)),
                created_by=created_users['sales_manager']
            )

            invoice = Invoice.objects.create(
                sales_order=order,
                invoice_number=f'INV{i+1:03d}',
                invoice_date=timezone.now(),
                due_date=timezone.now() + timedelta(days=30),
                amount=order.total_amount
            )

            Payment.objects.create(
                invoice=invoice,
                amount=invoice.amount,
                payment_date=timezone.now(),
                payment_method='Bank Transfer'
            )

        # Create suppliers and purchase data
        for i in range(5):
            supplier = Supplier.objects.create(
                name=f'Supplier {i+1}',
                email=f'supplier{i+1}@example.com',
                phone=f'+1555{random.randint(1000000, 9999999)}',
                address=f'Supplier {i+1} Address'
            )

            purchase_order = PurchaseOrder.objects.create(
                supplier=supplier,
                order_number=f'PO{i+1:03d}',
                order_date=timezone.now(),
                total_amount=Decimal(random.randint(1000, 10000)),
                created_by=created_users['purchase_manager']
            )

            Bill.objects.create(
                purchase_order=purchase_order,
                bill_number=f'BILL{i+1:03d}',
                bill_date=timezone.now(),
                due_date=timezone.now() + timedelta(days=30),
                amount=purchase_order.total_amount
            )

        # Create financial reports
        report_types = ['balance_sheet', 'income_statement', 'cash_flow', 'trial_balance']
        for report_type in report_types:
            FinancialReport.objects.create(
                report_type=report_type,
                start_date=timezone.now().date() - timedelta(days=30),
                end_date=timezone.now().date(),
                generated_by=created_users['accountant'],
                data={'sample': 'data'},
                notes=f'Sample {report_type.replace("_", " ").title()} report'
            )

        self.stdout.write(self.style.SUCCESS('Successfully created sample data')) 