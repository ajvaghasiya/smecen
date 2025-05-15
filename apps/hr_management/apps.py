from django.apps import AppConfig

class HrManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hr_management'
    verbose_name = 'HR Management'

    def ready(self):
        import apps.hr_management.signals 