from django.db import models
from .marks import Mark


class Model(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Модель',
        db_index=True,
    )
    mark = models.ForeignKey(Mark,
                             on_delete=models.CASCADE,
                             verbose_name='Марка',
                             )
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Отображать',
        db_index=True,
    )
    parts = models.ManyToManyField(
        'Part',
        related_name='models',
        verbose_name='Запчасти',
    )

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
