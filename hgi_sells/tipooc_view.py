
from hgi2.utils import get_user_from_usertoken
from hgi_sells.models import TypeOC
from hgi_sells.serializer import TypeOCSerializer
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


class TypeOCViewSet(viewsets.ModelViewSet):
    queryset = TypeOC.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = TypeOCSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = TypeOC.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        return JsonResponse({"type_oc":data_ppto}, status=200)
    
    def create(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Request error': str(error)},status=400)
        if "user" not in data.keys():
            if 'Authorization' in request.headers:
                user = get_user_from_usertoken(request.headers['Authorization'])
                data['user'] = user.id
            else:
                return JsonResponse ({'status_text':'No usaste token'}, status=403)
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            type_oc_data = serializer.data
            response = {'type_oc': type_oc_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)