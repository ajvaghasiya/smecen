from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.finance.models import Account, JournalEntry, JournalItem
from decimal import Decimal

class FinanceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='accountant',
            email='accountant@example.com',
            password='testpass123'
        )
        
        # Create test accounts
        self.cash_account = Account.objects.create(
            name='Cash',
            code='1000',
            type='asset',
            balance=Decimal('10000.00')
        )
        self.revenue_account = Account.objects.create(
            name='Revenue',
            code='4000',
            type='revenue',
            balance=Decimal('0.00')
        )

    def test_account_creation(self):
        """Test account creation"""
        self.assertEqual(self.cash_account.name, 'Cash')
        self.assertEqual(self.cash_account.type, 'asset')
        self.assertEqual(self.cash_account.balance, Decimal('10000.00'))

    def test_journal_entry(self):
        """Test journal entry creation"""
        entry = JournalEntry.objects.create(
            date='2024-01-01',
            reference='SALE001',
            description='Test Sale',
            created_by=self.user
        )
        
        # Create debit and credit items
        debit_item = JournalItem.objects.create(
            entry=entry,
            account=self.cash_account,
            debit=Decimal('1000.00'),
            credit=Decimal('0.00')
        )
        credit_item = JournalItem.objects.create(
            entry=entry,
            account=self.revenue_account,
            debit=Decimal('0.00'),
            credit=Decimal('1000.00')
        )

        self.assertEqual(entry.total_debit(), Decimal('1000.00'))
        self.assertEqual(entry.total_credit(), Decimal('1000.00'))
        self.assertTrue(entry.is_balanced()) 