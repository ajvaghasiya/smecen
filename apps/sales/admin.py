from django.contrib import admin
from .models import Customer, SalesOrder, Invoice, Payment

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'order_date', 'total_amount', 'created_by')
    list_filter = ('order_date', 'created_by')
    search_fields = ('order_number', 'customer__name')
    ordering = ('-order_date',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'sales_order', 'invoice_date', 'due_date', 'amount')
    list_filter = ('invoice_date', 'due_date')
    search_fields = ('invoice_number', 'sales_order__order_number')
    ordering = ('-invoice_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_date', 'payment_method')
    search_fields = ('invoice__invoice_number',)
    ordering = ('-payment_date',) 