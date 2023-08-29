
from hgi_static.models import ChangeManagement
from hgi_static.serializer import ChangeManagementSerializer
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

class ChangeManagementViewSet(viewsets.ModelViewSet):
    queryset = ChangeManagement.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ChangeManagementSerializer
    http_method_names = ["get", "patch", "post"]

    def retrieve(self, request, pk):
        self.queryset = ChangeManagement.objects.all()
        gestion_cambio = self.get_object()
        gestion_cambio_data = self.serializer_class(gestion_cambio).data
        return JsonResponse({"gestion_cambio":gestion_cambio_data}, status=200)
    
    def get_queryset(self):
        self.get_queryset = ChangeManagement.objects.all().order_by("-date_now")
        gestion_cambios = self.queryset

        if 'id' in self.request.query_params.keys():
            id = self.request.query_params['id']
        else:
            return gestion_cambios
        
        if 'contract' in self.request.query_params.keys():
            contract = self.request.query_params['contract']
            gestion_cambios = gestion_cambios.filter(type_model = "Contract").filter(obj_id=id)
        
        elif 'building_site' in self.request.query_params.keys():
            building_site = self.request.query_params['building_site']
            gestion_cambios = gestion_cambios.filter(type_model = "BuildingSite").filter(obj_id=id)
        
        elif 'oc' in self.request.query_params.keys():
            building_site = self.request.query_params['oc']
            gestion_cambios = gestion_cambios.filter(type_model = "Oc").filter(obj_id=id)
        
        elif 'client' in self.request.query_params.keys():
            client = self.request.query_params['client']
            gestion_cambios = gestion_cambios.filter(type_model = "Client").filter(obj_id=id)
        
        elif 'supplier' in self.request.query_params.keys():
            supplier = self.request.query_params['supplier']
            gestion_cambios = gestion_cambios.filter(type_model = "Supplier").filter(obj_id=id)
        
        elif 'cajachica' in self.request.query_params.keys():
            caja_chica = self.request.query_params['cajachica']
            gestion_cambios = gestion_cambios.filter(type_model = "CajaChica").filter(obj_id=id)
        
        elif 'budget' in self.request.query_params.keys():
            budget = self.request.query_params['budget']
            gestion_cambios = gestion_cambios.filter(type_model = "Budget").filter(obj_id=id)
        
        elif 'prodresource' in self.request.query_params.keys():
            prodresource = self.request.query_params['prodresource']
            gestion_cambios = gestion_cambios.filter(type_model = "ProdResource").filter(obj_id=id)
        
        elif 'itemcc' in self.request.query_params.keys():
            itemcc = self.request.query_params['itemcc']
            gestion_cambios = gestion_cambios.filter(type_model = "ItemCC").filter(obj_id=id)
        
        elif 'itemresource' in self.request.query_params.keys():
            itemresource = self.request.query_params['itemresource']
            gestion_cambios = gestion_cambios.filter(type_model = "ItemResource").filter(obj_id=id)
        
        elif 'productoc' in self.request.query_params.keys():
            productoc = self.request.query_params['productoc']
            gestion_cambios = gestion_cambios.filter(type_model = "ProductOc").filter(obj_id=id)
        
        return gestion_cambios

    def list(self, request):
        gestion_cambio = self.get_queryset()
        pages = Paginator(gestion_cambio, 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        gestion_cambio_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(gestion_cambio_all, many=True)
        response_data = serializer.data
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)