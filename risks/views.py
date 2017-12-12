from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe
from django.http import JsonResponse

from .models import Risk

@require_safe
def index(request):
    response_data = []
    risks = Risk.objects.all().prefetch_related('textfields', 'numberfields', 'datetimefields', 'enumfields')
    for risk in risks:
        response_data.append(risk.get_data())
    return JsonResponse(response_data, safe=False)

@require_safe
def show(request, risk_id):
    risk = get_object_or_404(Risk, pk=risk_id)
    return JsonResponse(risk.get_data())
