from django.contrib import admin
from .models import Supplier, PurchaseOrder, Bill, BillPayment

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'supplier', 'order_date', 'total_amount', 'created_by')
    list_filter = ('order_date', 'created_by')
    search_fields = ('order_number', 'supplier__name')
    ordering = ('-order_date',)

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'purchase_order', 'bill_date', 'due_date', 'amount')
    list_filter = ('bill_date', 'due_date')
    search_fields = ('bill_number', 'purchase_order__order_number')
    ordering = ('-bill_date',)

@admin.register(BillPayment)
class BillPaymentAdmin(admin.ModelAdmin):
    list_display = ('bill', 'payment_date', 'amount', 'payment_method')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('bill__bill_number', 'reference') 