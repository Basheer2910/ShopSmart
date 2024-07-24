from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helper.fetch import fetch_products

@api_view(['GET'])
def get_products(request):
    product_name = request.GET.get('product_name', '')
    if not product_name:
        return Response({'error': 'Product name is required'}, status=400)
    
    products = fetch_products(product_name)
    # print(products)
    return Response(products)
