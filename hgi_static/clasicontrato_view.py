
from hgi_static.models import ClasiContract
from hgi_static.serializer import ClasiContractSerializer
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


class ClasiContractViewSet(viewsets.ModelViewSet):
    queryset = ClasiContract.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ClasiContractSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = ClasiContract.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        return JsonResponse({"clasicontract":data_ppto}, status=200)