

from hgi2.utils import get_changes_list, register_change, get_user_from_usertoken
from hgi_users.models import Supplier
from hgi_users.serializer import SupplierSerializer
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


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = SupplierSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Supplier.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        return JsonResponse({"supplier":data_ppto}, status=200)
    
    def create(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Request error': str(error)},status=400)
        
        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
            if "creator" not in data.keys():
                data['creator'] = user.id
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            supplier_data = serializer.data
            register_change(supplier_data["id"],[1,],user,"Supplier")
            response = {'supplier': supplier_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = Supplier.objects.all()
        supplier = self.get_object()

        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        serializer = self.serializer_class(supplier, data=request.data, partial=True)
        changes = get_changes_list(request.data)
        if serializer.is_valid():
            serializer.save()
            supplier_data = serializer.data
            register_change(supplier_data["id"],changes,user,"Supplier")
            return JsonResponse({"status_text": "Supplier editado con exito.", "supplier": supplier_data,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400)