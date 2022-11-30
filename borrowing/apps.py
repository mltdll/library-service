from django.apps import AppConfig
from django.db.models.signals import post_migrate


def post_migrate_schedule_tasks(sender, **kwargs):
    from .scheduled_tasks import schedule_tasks
    schedule_tasks()


class BorrowingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrowing"

    def ready(self):
        post_migrate.connect(post_migrate_schedule_tasks, sender=self)
