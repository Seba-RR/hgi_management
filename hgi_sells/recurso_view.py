
from hgi_sells.models import Resource
from hgi_sells.serializer import ResourceSerializer
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
from django.db.models import Q


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ResourceSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Resource.objects.all()
        resource = self.get_object()
        data_resource = self.serializer_class(resource).data
        return JsonResponse({"resource":data_resource}, status=200)
    
    def get_queryset(self):
        self.get_queryset = Resource.objects.filter(is_main=True)
        resources = self.queryset

        if "search" in self.request.query_params.keys():
            description_query = Q(description__contains=self.request.query_params["search"])
            resources = resources.filter(description_query)
            
        return resources
    
    def list(self, request):
        resources = self.get_queryset()
        pages = Paginator(resources, 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        resources_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(resources_all, many=True)
        response_data = serializer.data
        for resource in response_data:
            sub_resources = Resource.objects.filter(resource=resource['id'])
            sub_resources_data = ResourceSerializer(sub_resources, many=True).data
            resource["sub_resources"] = sub_resources_data
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)