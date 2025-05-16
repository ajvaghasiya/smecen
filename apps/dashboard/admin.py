from django.contrib import admin
from .models import DashboardWidget, UserDashboard, UserDashboardWidget, Notification, Activity

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'widget_type', 'is_active', 'created_at')
    list_filter = ('widget_type', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(UserDashboard)
class UserDashboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)

@admin.register(UserDashboardWidget)
class UserDashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('dashboard', 'widget', 'position', 'is_visible')
    list_filter = ('is_visible',)
    search_fields = ('dashboard__user__username', 'widget__name')
    ordering = ('dashboard', 'position')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    ordering = ('-created_at',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'model_name', 'created_at')
    list_filter = ('activity_type', 'model_name', 'created_at')
    search_fields = ('user__username', 'description')
    ordering = ('-created_at',) 