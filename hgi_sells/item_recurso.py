

from hgi_sells.models import ProdResource
from hgi2.utils import get_user_from_usertoken
from hgi_sells.models import ItemResource
from hgi_sells.serializer import ItemResourceSerializer
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

class ItemResourceViewSet(viewsets.ModelViewSet):
    queryset = ItemResource.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ItemResourceSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ItemResource.objects.all()
        item = self.get_object()
        data_item = self.serializer_class(item).data
        return JsonResponse({"item_rec":data_item}, status=200)
    
    def get_queryset(self):
        self.get_queryset = ItemResource.objects.all()
        items = self.queryset

        if 'batch' in self.request.query_params.keys():
            batch = self.request.query_params['batch']
            items = items.filter(batch = batch)

        if 'prodresource' in self.request.query_params.keys():
            prodresource = self.request.query_params['prodresource']
            items = items.filter(resource = prodresource)
            
        return items

    def list(self, request):
        items = self.get_queryset()
        pages = Paginator(items.order_by('date_now').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        items_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(items_all, many=True)
        response_data = serializer.data
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = ItemResource.objects.all()
        item = self.get_object()
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_item = serializer.data
            return JsonResponse({"status_text": "ItemResource editado con exito.", "item_rec": data_item,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400) 
        
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

        prod_resource = ProdResource.objects.get(id=data['resource'])
        if "batch" not in data.keys():
            data['batch'] = prod_resource.batch.id
        if "contract" not in data.keys():
            data['contract'] = prod_resource.batch.contract.id
            
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            item_rec_data = serializer.data
            return JsonResponse({"item_rec":item_rec_data}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)