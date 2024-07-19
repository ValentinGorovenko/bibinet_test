from django.db import models
from .car_models import Model
from .marks import Mark


class Part(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        db_index=True,
    )
    mark = models.ManyToManyField(
        Mark,
        verbose_name='Марки',
    )
    model = models.ManyToManyField(
        Model,
        verbose_name='Модели',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
    )
    json_data = models.JSONField(
        default=dict,
    )
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Отображать',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
