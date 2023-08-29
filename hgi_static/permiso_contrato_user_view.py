
from hgi_static.serializer import PermissionContractUserSerializer
from hgi_static.models import PermissionContractUser
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


class PermissionContractUserViewSet(viewsets.ModelViewSet):
    queryset = PermissionContractUser.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = PermissionContractUserSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = PermissionContractUser.objects.all()
        permiso_user = self.get_object()
        data_permiso_user = self.serializer_class(permiso_user).data
        return JsonResponse({"permiso_user":data_permiso_user}, status=200)
    
    def get_queryset(self):
        self.get_queryset = PermissionContractUser.objects.all()
        permissions = self.queryset

        if 'user' in self.request.query_params.keys():
            user = self.request.query_params['user']
            permissions = permissions.filter(contract = user)
            
        return permissions

    def list(self, request):
        permissions = self.get_queryset()
        pages = Paginator(permissions.reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        permissions_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(permissions_all, many=True)
        response_data = serializer.data

        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)