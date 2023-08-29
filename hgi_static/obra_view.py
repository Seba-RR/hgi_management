from hgi2.utils import get_changes_list, register_change, get_user_from_usertoken
from hgi_users.models import Client
from hgi_static.models import BuildingSite
from hgi_static.serializer import BuildingSiteSerializer
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


class BuildingSiteViewSet(viewsets.ModelViewSet):
    queryset = BuildingSite.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = BuildingSiteSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = BuildingSite.objects.all()
        building_site = self.get_object()
        data_building_site = self.serializer_class(building_site).data
        client = Client.objects.get(id=data_building_site['client'])
        data_building_site['client_name'] = client.business_name
        return JsonResponse({"building_site":data_building_site}, status=200)
    
    def get_queryset(self):
        queryset = BuildingSite.objects.all()
        building_sites = queryset

        if 'company' in self.request.query_params.keys():
            company = self.request.query_params['company']
            building_sites = building_sites.filter(company = company) 
        
        return building_sites
    
    def list(self, request):
        user = get_user_from_usertoken(request.headers["Authorization"])
        building_sites = self.get_queryset()
        if user.company is not None:
            building_sites = building_sites.filter(company=user.company)
        pages = Paginator(building_sites.order_by('date_now').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        building_sites_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(building_sites_all, many=True)
        response_data = serializer.data
        for building_site in response_data:
            client = Client.objects.get(id=building_site['client'])
            building_site['client_name'] = client.business_name
        
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)
    
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
            building_site_data = serializer.data
            register_change(building_site_data["id"],[1,],user,"BuildingSite")
            response = {'building_site': building_site_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = BuildingSite.objects.all()
        building_site = self.get_object()

        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        serializer = self.serializer_class(building_site, data=request.data, partial=True)
        changes = get_changes_list(request.data)
        if serializer.is_valid():
            serializer.save()
            building_site_data = serializer.data
            register_change(building_site_data["id"],changes,user,"BuildingSite")
            return JsonResponse({"status_text": "BuildingSite editada con exito.", "building_site": building_site_data,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400)
        
    def destroy(self, request, *args, **kwargs):
        self.queryset = BuildingSite.objects.all()
        building_site = self.get_object()
        if building_site is not None:
            building_site.delete()
            return JsonResponse({'status_text': 'BuildingSite eliminada correctamente'}, status=200)

