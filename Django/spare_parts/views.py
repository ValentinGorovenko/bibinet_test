import json
from itertools import product

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from spare_parts.models import Mark, Model, Part


def mark_list(request):
    marks = Mark.objects.all().values('id', 'name', 'producer_country_name').filter(is_visible=True)
    return JsonResponse({'marks': list(marks)})


def model_list(request):
    models = Model.objects.all().values('id', 'name', 'mark__name').filter(is_visible=True)
    return JsonResponse({'models': list(models)})


@csrf_exempt
def search_part(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        page = data.get("page", 1)
        page_size = 10
        offset = (page - 1) * page_size

        query = Q()

        mark_name = data.get("mark_name")
        if mark_name:
            query &= Q(mark__name__icontains=mark_name)

        part_name = data.get("part_name")
        if part_name:
            query &= Q(name__icontains=part_name)

        params = data.get("params", {})
        if 'is_new_part' in params:
            query &= Q(json_data__is_new_part=params['is_new_part'])
        if 'color' in params:
            color = params['color']
            query &= Q(json_data__color__iexact=color)

        price_gte = data.get("price_gte")
        if price_gte is not None:
            query &= Q(price__gte=price_gte)

        price_lte = data.get("price_lte")
        if price_lte is not None:
            query &= Q(price__lte=price_lte)

        parts = Part.objects.filter(query).distinct()[offset:offset + page_size]
        total_count = Part.objects.filter(query).distinct().count()
        total_sum = sum(part.price for part in parts)

        response_data = []
        for part in parts:
            marks = list(part.mark.all())
            models = list(part.model.all())

            for mark, model in product(marks, models):
                response_data.append({
                    "mark": {
                        "id": mark.id,
                        "name": mark.name,
                        "producer_country_name": mark.producer_country_name
                    },
                    "model": {
                        "id": model.id,
                        "name": model.name
                    },
                    "name": part.name,
                    "json_data": part.json_data,
                    "price": str(part.price)
                })
        return JsonResponse({
            "response": response_data,
            "count": total_count,
            "summ": total_sum
        })
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
