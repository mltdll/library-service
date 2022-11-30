from django.apps import AppConfig


class BorrowingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrowing"

    def ready(self):
        from .scheduled_tasks import schedule_tasks

        # Schedule all the necessary tasks at the startup of the project
        schedule_tasks()
