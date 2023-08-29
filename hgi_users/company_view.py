

from hgi_users.models import Company
from hgi_users.serializer import CompanySerializer
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


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = CompanySerializer
    http_method_names = ["get", "patch", "post"]

    def retrieve(self, request, pk):
        self.queryset = Company.objects.all()
        company = self.get_object()
        data_company = self.serializer_class(company).data
        return JsonResponse({"company":data_company}, status=200)
    
    def get_queryset(self):
        self.get_queryset = Company.objects.all().order_by("-date_now_creado")
        companys = self.queryset

        if "search" in self.request.query_params.keys():
            name_query = Q(name__contains=self.request.query_params["search"])
            companys = companys.filter(name_query)
            
        return companys
    
    def list(self, request):
        companys = self.get_queryset()
        pages = Paginator(companys, 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        companys_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(companys_all, many=True)
        response_data = serializer.data
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)