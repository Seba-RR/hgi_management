
from hgi2.utils import get_user_from_usertoken
from hgi_sells.models import ProductOC
from hgi_sells.serializer import ProductOCSerializer
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
from django.db.models import Q


class ProductOCViewSet(viewsets.ModelViewSet):
    queryset = ProductOC.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductOCSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ProductOC.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        return JsonResponse({"product_oc":data_ppto}, status=200)

    def get_queryset(self):
        self.get_queryset = ProductOC.objects.all()
        products = self.queryset

        if 'batch' in self.request.query_params.keys():
            batch = self.request.query_params['batch']
            products = products.filter(batch = batch)

        if 'oc' in self.request.query_params.keys():
            oc = self.request.query_params['oc']
            products = products.filter(oc = oc)
        
        if 'contract' in self.request.query_params.keys():
            contract = self.request.query_params['contract']
            products = products.filter(batch__contract = contract)

        if "search" in self.request.query_params.keys():
            text_query = Q(product__contains=self.request.query_params["search"])
            products = products.filter(text_query)
            
        return products

    def list(self, request):
        products = self.get_queryset()
        pages = Paginator(products.order_by('date_entrance').reverse(), 99999)
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
            
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            product_data = serializer.data
            response = {'product_oc': product_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = ProductOC.objects.all()
        product = self.get_object()
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_product = serializer.data
            return JsonResponse({"status_text": "ProductOC editado con exito.", "product_oc": data_product,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400) 