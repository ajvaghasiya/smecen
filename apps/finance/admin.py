from django.contrib import admin
from .models import (
    Account, JournalEntry, JournalItem, BankAccount, BankReconciliation,
    Transaction, TransactionLine, ExpenseClaim, ExpenseClaimLine, FinancialReport
)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'type', 'balance', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('code', 'name')
    ordering = ('code',)

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'reference', 'description', 'total_amount', 'created_by')
    list_filter = ('date', 'created_by')
    search_fields = ('reference', 'description')
    ordering = ('-date',)

    def total_amount(self, obj):
        return sum(item.debit for item in obj.journalitem_set.all())

@admin.register(JournalItem)
class JournalItemAdmin(admin.ModelAdmin):
    list_display = ('journal_entry', 'account', 'debit', 'credit')
    list_filter = ('account',)
    search_fields = ('journal_entry__reference', 'account__name')
    ordering = ('journal_entry', 'account')

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank_name', 'account_number', 'balance')
    search_fields = ('name', 'bank_name', 'account_number')
    ordering = ('name',)

@admin.register(BankReconciliation)
class BankReconciliationAdmin(admin.ModelAdmin):
    list_display = ('bank_account', 'statement_date', 'statement_balance', 'reconciled_balance', 'is_reconciled')
    list_filter = ('is_reconciled', 'statement_date')
    search_fields = ('bank_account__name', 'bank_account__account_number')
    ordering = ('-statement_date',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'transaction_type', 'date', 'created_by')
    list_filter = ('transaction_type', 'date')
    search_fields = ('reference_number', 'description')
    ordering = ('-date',)

@admin.register(TransactionLine)
class TransactionLineAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'account', 'description', 'debit', 'credit')
    list_filter = ('account',)
    search_fields = ('transaction__reference_number', 'account__name', 'description')
    ordering = ('transaction', 'account')

@admin.register(ExpenseClaim)
class ExpenseClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_number', 'employee', 'date', 'total_amount', 'status')
    list_filter = ('status', 'date')
    search_fields = ('claim_number', 'employee__user__username', 'description')
    ordering = ('-date',)

@admin.register(ExpenseClaimLine)
class ExpenseClaimLineAdmin(admin.ModelAdmin):
    list_display = ('claim', 'expense_date', 'category', 'amount')
    list_filter = ('category', 'expense_date')
    search_fields = ('claim__claim_number', 'description', 'category')
    ordering = ('-expense_date',)

@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'start_date', 'end_date', 'generated_by', 'generated_at')
    list_filter = ('report_type', 'start_date', 'end_date')
    search_fields = ('report_type', 'notes')
    ordering = ('-generated_at',) 