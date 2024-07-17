from django.db import models


class Mark(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Марка',
        )
    producer_country_name = models.CharField(
        max_length=100,
        verbose_name='Страна производства',
        )
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Отображать',
        )
    parts = models.ManyToManyField(
        'Part',
        related_name='marks',
        verbose_name='Запчасти',
        )

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'
