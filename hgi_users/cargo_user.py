
from hgi_users.serializer import CargoUserSerializer
from hgi_users.models import CargoUser
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


class CargoUserViewSet(viewsets.ModelViewSet):
    queryset = CargoUser.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = CargoUserSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = CargoUser.objects.all()
        cargo = self.get_object()
        data_cargo = self.serializer_class(cargo).data
        return JsonResponse({"cargo":data_cargo}, status=200)