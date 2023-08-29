
from hgi_users.models import PermissionContract
from hgi_users.serializer import PermissionContractSerializer
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


class PermissionContractViewSet(viewsets.ModelViewSet):
    queryset = PermissionContract.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = PermissionContractSerializer
    http_method_names = ["get", "patch", "post"]

    def retrieve(self, request, pk):
        self.queryset = PermissionContract.objects.all()
        permiso = self.get_object()
        data_permiso = self.serializer_class(permiso).data
        return JsonResponse({"permiso":data_permiso}, status=200)