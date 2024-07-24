from django.core.management import BaseCommand
from spare_parts.models import Mark, Model


class Command(BaseCommand):
    MARKS = [
        {'name': 'Toyota', 'producer_country_name': 'Japan', 'is_visible': True},
        {'name': 'Honda', 'producer_country_name': 'Japan', 'is_visible': True},
        {'name': 'Mercedes', 'producer_country_name': 'Germany', 'is_visible': True},
        {'name': 'Ford', 'producer_country_name': 'USA', 'is_visible': True},
        {'name': 'Москвич', 'producer_country_name': 'Russia', 'is_visible': True},
    ]
    MODELS = [
        {'name': 'Yaris', 'mark': 'Toyota', 'is_visible': True},
        {'name': 'Accord', 'mark': 'Honda', 'is_visible': True},
        {'name': 'Sprinter', 'mark': 'Mercedes', 'is_visible': True},
        {'name': 'Explorer', 'mark': 'Ford', 'is_visible': True},
        {'name': '412', 'mark': 'Москвич', 'is_visible': True},
    ]

    def handle(self, *args, **kwargs):
        for mark_data in self.MARKS:
            mark_obj = Mark.objects.create(**mark_data)
        self.stdout.write(self.style.SUCCESS('Макри автомобилей загружены.'))

        for model_data in self.MODELS:
            mark_name = model_data.pop('mark')
            mark_obj = Mark.objects.get(name=mark_name)
            model_data['mark'] = mark_obj
            Model.objects.create(**model_data)
        self.stdout.write(self.style.SUCCESS('Модели автомобилей загружены.'))
