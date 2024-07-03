import json
from django.http import JsonResponse, Http404
from external_api_services.services.nova_poshta_api_service import CitySearcher, StreetSearcher, DepartmentSearcher


def city_autocomplete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        searcher = CitySearcher({'query': data.get('query')})
        autocomplete_data = searcher.get_response_from_API()
        return JsonResponse(autocomplete_data, safe=False)
    else:
        raise Http404()


def street_autocomplete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        searcher = StreetSearcher({'query': data.get('query'), 'city_id': data.get('city_id')})
        autocomplete_data = searcher.get_response_from_API()
        return JsonResponse(autocomplete_data, safe=False)
    else:
        raise Http404()


def department_autocomplete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        searcher = DepartmentSearcher({'query': data.get('query'), 'city_id': data.get('city_id')})
        autocomplete_data = searcher.get_response_from_API()
        return JsonResponse(autocomplete_data, safe=False)
    else:
        raise Http404()
