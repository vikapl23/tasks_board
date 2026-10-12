from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tasks.models import Board, Comment, Task


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        if Task.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists, skipping.'))
            return

        anna = self.get_user('anna')
        bohdan = self.get_user('bohdan')

        work, _ = Board.objects.get_or_create(name='Work')
        study, _ = Board.objects.get_or_create(name='Study')
        home, _ = Board.objects.get_or_create(name='Home')

        today = date.today()

        def day(offset):
            return today + timedelta(days=offset)

        report = Task.objects.create(title='Написати звіт', board=work, status='in_progress',
                                     start_date=day(-5), deadline=day(10), owner=anna)
        Task.objects.create(title='Підготувати презентацію', board=work, status='todo',
                            start_date=day(-2), deadline=day(7), owner=anna)
        Task.objects.create(title='Відповісти на листи', board=work, status='done',
                            start_date=day(-10), deadline=day(-8), owner=bohdan)
        homework = Task.objects.create(title='Здати ДЗ з DRF', board=study, status='todo',
                                       start_date=day(-14), deadline=day(-3), owner=anna)
        Task.objects.create(title='Прочитати документацію Docker', board=study, status='todo',
                            start_date=day(0), deadline=day(14), owner=bohdan)
        Task.objects.create(title='Встановити Postman', board=study, status='done',
                            start_date=day(-7), deadline=day(-1), owner=bohdan)
        tickets = Task.objects.create(title='Купити квитки', board=home, status='todo',
                                      start_date=day(-20), deadline=day(-12), owner=bohdan)
        Task.objects.create(title='Полити квіти', board=home, status='in_progress',
                            start_date=day(-1), deadline=day(1), owner=anna)

        Comment.objects.create(task=report, text='Чернетка готова, лишились висновки', owner=anna)
        Comment.objects.create(task=report, text='Додай, будь ласка, графік за вересень', owner=bohdan)
        Comment.objects.create(task=homework, text='Дедлайн уже минув, треба поспішити', owner=bohdan)
        Comment.objects.create(task=tickets, text='Подивись ранкові рейси', owner=anna)

        self.stdout.write(self.style.SUCCESS('Done.'))

    def get_user(self, username):
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('pass12345')
            user.save()
        return user