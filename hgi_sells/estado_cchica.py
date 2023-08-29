
from hgi2.utils import get_user_from_usertoken
from hgi_sells.models import EstadoCajaChica
from hgi_sells.serializer import EstadoCajaChicaSerializer
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


class EstadoCajaChicaViewSet(viewsets.ModelViewSet):
    queryset = EstadoCajaChica.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = EstadoCajaChicaSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = EstadoCajaChica.objects.all()
        resource = self.get_object()
        state_cchica_data = self.serializer_class(resource).data
        return JsonResponse({"state_cchica":state_cchica_data}, status=200)
    
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
            
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            state_cchica_data = serializer.data
            response = {'state_cchica': state_cchica_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)