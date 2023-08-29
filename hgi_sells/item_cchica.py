
from hgi2.utils import get_user_from_usertoken
from hgi_sells.models import CajaChica
from hgi_static.models import Contract
from hgi_sells.models import ItemCajaChica
from hgi_sells.serializer import ItemCajaChicaSerializer
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

class ItemCajaChicaViewSet(viewsets.ModelViewSet):
    queryset = ItemCajaChica.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ItemCajaChicaSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ItemCajaChica.objects.all()
        item = self.get_object()
        data_item = self.serializer_class(item).data
        data_item['name_batch'] = item.batch.description
        data_item['name_supplier'] = item.supplier.rs
        data_item['name_resource'] = item.resource.resource.description
        data_item['name_type'] = item.type.description
        return JsonResponse({"item_cch":data_item}, status=200)
    
    def get_queryset(self):
        self.get_queryset = ItemCajaChica.objects.all()
        items = self.queryset

        if 'caja' in self.request.query_params.keys():
            caja = self.request.query_params['caja']
            items = items.filter(caja_chica = caja)
            
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
        for data_item in response_data:
            item = ItemCajaChica.objects.get(id=data_item['id'])
            data_item['name_batch'] = item.batch.description
            data_item['name_supplier'] = item.supplier.rs
            data_item['name_resource'] = item.resource.resource.description
            data_item['name_type'] = item.type.description
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = ItemCajaChica.objects.all()
        item = self.get_object()
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_item = serializer.data
            return JsonResponse({"status_text": "ItemCajaChica editado con exito.", "item_cch": data_item,},status=202)
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
            
        caja_chica = CajaChica.objects.get(id=data['caja_chica'])
        data['contract'] = caja_chica.contract.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            item_cch_serializer = serializer.data
            return JsonResponse({"item_cch":item_cch_serializer}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)