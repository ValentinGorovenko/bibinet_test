import random
from django.core.management.base import BaseCommand
from spare_parts.models import Part, Mark, Model


class Command(BaseCommand):

    PART_NAMES = ['ДВС', 'Тормозной суппорт', 'Ступица', 'Крыло', 'Бампер']
    COLORS = ['Белый', 'Черный', 'Красный', 'Желтый', 'Зеленый']

    def handle(self, *args, **kwargs):
        marks = Mark.objects.all()
        models = Model.objects.all()

        for _ in range(10):
            random_mark = random.choice(marks)
            random_model = random.choice(models)
            part_name = random.choice(self.PART_NAMES)
            json_data = {
                'color': random.choice(self.COLORS),
                'is_new_part': random.choice([True, False]),
                'count': random.randint(1, 10),
            }
            price = random.randint(1000, 10000)
            part = Part.objects.create(name=part_name, price=price)
            part.mark.add(random_mark)
            part.model.add(random_model)
            part.json_data = json_data
            part.save()
        self.stdout.write(self.style.SUCCESS('Таблица запчастей успешно заполнена с 10 000 случайными записями.'))    
