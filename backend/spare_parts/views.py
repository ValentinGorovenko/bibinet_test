from django.http import JsonResponse
from spare_parts.models import Mark, Model


def mark_list(request):
    marks = Mark.objects.all().values('id', 'name', 'producer_country_name').filter(is_visible=True)
    return JsonResponse({'marks': list(marks)})


def model_list(request):
    models = Model.objects.all().values('id', 'name', 'mark__name').filter(is_visible=True)
    return JsonResponse({'models': list(models)})
