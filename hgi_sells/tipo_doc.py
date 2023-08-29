
from hgi_sells.models import TypeDocument
from hgi_sells.serializer import TypeDocumentSerializer
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


class TypeDocumentViewSet(viewsets.ModelViewSet):
    queryset = TypeDocument.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = TypeDocumentSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = TypeDocument.objects.all()
        type = self.get_object()
        data_type = self.serializer_class(type).data
        return JsonResponse({"type":data_type}, status=200)