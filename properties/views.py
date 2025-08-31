from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Property
from .serializers import PropertySerializer
from .utils import get_all_properties

@api_view(['GET'])
@cache_page(60 * 15)  # Cache the entire response for 15 minutes
def property_list(request):
    """
    List all properties with caching enabled.
    The queryset is cached for 1 hour, and the response is cached for 15 minutes.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    # Get properties from cache or database
    properties = get_all_properties()
    serializer = PropertySerializer(properties, many=True)
    return JsonResponse({'properties': serializer.data}, safe=False)