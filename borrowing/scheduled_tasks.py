from django_q.tasks import schedule


def schedule_tasks():
    """
    Schedule tasks that should always be on.
    """
    from django_q.models import Schedule

    # Schedule task only if no tasks like that are already up.
    if not Schedule.objects.filter(
        func="notification_service.notify.notify_overdue_borrowings"
    ).exists():
        schedule(
            "notification_service.notify.notify_overdue_borrowings",
            schedule_type=Schedule.DAILY,
        )
