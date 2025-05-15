from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class DashboardWidget(models.Model):
    WIDGET_TYPES = (
        ('sales_summary', 'Sales Summary'),
        ('purchase_summary', 'Purchase Summary'),
        ('expense_summary', 'Expense Summary'),
        ('cash_flow', 'Cash Flow'),
        ('profit_loss', 'Profit & Loss'),
        ('top_customers', 'Top Customers'),
        ('top_products', 'Top Products'),
        ('recent_activities', 'Recent Activities'),
        ('tasks', 'Tasks'),
        ('calendar', 'Calendar'),
    )

    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"

class UserDashboard(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widgets = models.ManyToManyField(DashboardWidget, through='UserDashboardWidget')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard for {self.user.get_full_name()}"

class UserDashboardWidget(models.Model):
    dashboard = models.ForeignKey(UserDashboard, on_delete=models.CASCADE)
    widget = models.ForeignKey(DashboardWidget, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    is_visible = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']
        unique_together = ['dashboard', 'position']

    def __str__(self):
        return f"{self.widget.name} - Position {self.position}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"

class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('complete', 'Completed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} {self.get_activity_type_display()} {self.model_name}" 