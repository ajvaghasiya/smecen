from django.contrib import admin
from .models import Employee, LeaveRequest, Attendance, Document

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'position', 'joining_date', 'salary')
    list_filter = ('department', 'position')
    search_fields = ('employee_id', 'user__username', 'user__email', 'department', 'position')
    ordering = ('employee_id',)

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('leave_type', 'status')
    search_fields = ('employee__employee_id', 'employee__user__username', 'reason')
    ordering = ('-created_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    list_filter = ('date', 'status')
    search_fields = ('employee__employee_id', 'employee__user__username')
    ordering = ('-date', 'employee')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('employee__employee_id', 'employee__user__username', 'title')
    ordering = ('-uploaded_at',) 