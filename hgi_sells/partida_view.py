
from hgi2.utils import get_user_from_usertoken
from hgi_sells.serializer import BatchSerializer
from hgi_sells.models import Batch
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
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = BatchSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Batch.objects.all()
        batch = self.get_object()
        data_batch = self.serializer_class(batch).data
        return JsonResponse({"batch":data_batch}, status=200)

    def get_queryset(self):
        self.get_queryset = Batch.objects.all()
        batchs = self.queryset

        if 'contract' in self.request.query_params.keys():
            contract = self.request.query_params['contract']
            batchs = batchs.filter(contract = contract)
            
        return batchs

    def list(self, request):
        batchs = self.get_queryset()
        pages = Paginator(batchs.order_by('start').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        batchs_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(batchs_all, many=True)
        response_data = serializer.data

        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)

    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = Batch.objects.all()
        batch = self.get_object()
        serializer = self.serializer_class(batch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_batch = serializer.data
            return JsonResponse({"status_text": "Batch editado con exito.", "batch": data_batch,},status=202)
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
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            batch_serializer = serializer.data
            return JsonResponse({"batch":batch_serializer}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)