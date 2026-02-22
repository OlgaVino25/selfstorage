import logging
from datetime import date, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from rent.models import Rent

logger = logging.getLogger(__name__)


def send_rent_email(user, subject, message):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Ошибка отправки почты для {user.email}: {e}")


def check_rent_notifications():
    today = date.today()

    for days in [30, 14, 7, 3]:
        target_date = today + timedelta(days=days)
        rents = Rent.objects.filter(
            end_date=target_date,
            is_active=True
        )
        for rent in rents:
            send_rent_email(
                rent.user,
                "Срок аренды скоро истекает",
                f"Напоминаем, что ваш срок аренды бокса истекает {rent.end_date}. "
                f"Пожалуйста, заберите вещи вовремя."
            )

    expired_today = Rent.objects.filter(end_date=today, is_active=True)
    for rent in expired_today:
        send_rent_email(
            rent.user,
            "Срок аренды истек сегодня",
            "С завтрашнего дня вещи будут храниться по повышенному тарифу в течение 6 месяцев. "
            "Если вы не заберете их, они будут утилизированы."
        )

    overdue_rents = Rent.objects.filter(end_date__lt=today, is_active=True)
    for rent in overdue_rents:
        days_overdue = (today - rent.end_date).days
        if days_overdue % 30 == 0:
            send_rent_email(
                rent.user,
                "Внимание: вещи все еще на складе",
                f"Ваш срок аренды истек {days_overdue} дней назад. "
                "Мы продолжаем хранить ваши вещи, но просим забрать их как можно скорее."
            )


class Command(BaseCommand):
    help = "Запускает планировщик для рассылки уведомлений по аренде"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        scheduler.add_job(
            check_rent_notifications,
            trigger=CronTrigger(hour=10, minute=0),
            id="check_rent_notifications",
            name="Daily rent check",
            replace_existing=True,
        )

        try:
            self.stdout.write("Запуск планировщика уведомлений...")
            scheduler.start()
        except KeyboardInterrupt:
            self.stdout.write("Планировщик остановлен.")
            scheduler.shutdown()
