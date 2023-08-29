

from hgi_sells.models import Resource
from hgi2.utils import get_user_from_usertoken
from hgi_sells.serializer import ProdResourceSerializer
from hgi_sells.models import ProdResource
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    action,
)
from django.views.decorators.csrf import csrf_exempt
import json
from json.decoder import JSONDecodeError
from django.http.response import JsonResponse
from rest_framework import viewsets, permissions
from django.core.paginator import Paginator

class ProdResourceViewSet(viewsets.ModelViewSet):
    queryset = ProdResource.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProdResourceSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ProdResource.objects.all()
        prod_resource = self.get_object()
        data_prod_resource = self.serializer_class(prod_resource).data
        resource = Resource.objects.get(id=data_prod_resource['resource'])
        data_prod_resource['code_resource'] = resource.code
        data_prod_resource['name_resource'] = resource.description
        return JsonResponse({"prod_resource":data_prod_resource}, status=200)
    
    def get_queryset(self):
        self.get_queryset = ProdResource.objects.all()
        products = self.queryset

        if 'batch' in self.request.query_params.keys():
            batch = self.request.query_params['batch']
            products = products.filter(batch = batch)
            
        return products

    def list(self, request):
        products = self.get_queryset()
        pages = Paginator(products.order_by('start').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        products_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(products_all, many=True)
        response_data = serializer.data
        for product in response_data:
            resource = Resource.objects.get(id=product['resource'])
            product['code_resource'] = resource.code
            product['name_resource'] = resource.description
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)
    
    def create(self, request):

        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Request error': str(error)},status=400)
        
        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        if "creator" not in data.keys():
            data['creator'] = user.id
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            prod_resource_data= serializer.data
            return JsonResponse({"prod_resource":prod_resource_data}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)