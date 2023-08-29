
from hgi2.utils import get_user_from_usertoken
from hgi2.utils import get_total_batchs_APU
from hgi_sells.models import Batch
from hgi_static.serializer import TypeBudgetSerializer
from hgi_sells.serializer import BudgetSerializer
from hgi_static.models import TypeBudget, Contract
from hgi_sells.models import Budget
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
from django.db.models import Q
from django.core.paginator import Paginator


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = BudgetSerializer
    http_method_names = ["get", "patch", "delete", "post"]
  
    def retrieve(self, request, pk):
        self.queryset = Budget.objects.all()
        ppto = self.get_object()
        data_ppto = self.serializer_class(ppto).data
        type = TypeBudget.objects.get(id=data_ppto['type'])
        data_ppto['type'] = TypeBudgetSerializer(type).data
        return JsonResponse({"budget":data_ppto}, status=200)

    def get_queryset(self):
        self.get_queryset = Budget.objects.all()
        budgets = self.queryset

        if 'contract' in self.request.query_params.keys():
            contract = self.request.query_params['contract']
            budgets = budgets.filter(contract = contract)

        if 'type' in self.request.query_params.keys():
            type = self.request.query_params['type']
            budgets = budgets.filter(type = type)
        
        if "search" in self.request.query_params.keys():
            text_query = Q(description__contains=self.request.query_params["description"])
            budgets = budgets.filter(text_query)
            
        return budgets

    def list(self, request):
        budgets = self.get_queryset()
        pages = Paginator(budgets.reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        budgets_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(budgets_all, many=True)
        response_data = serializer.data
        for budget in response_data:
            contract = Contract.objects.get(id=budget["contract"])
            batchs = Batch.objects.filter(contract=contract)
            budget["total_batchs"], budget["total_APU"] = get_total_batchs_APU(batchs)
            budget["n_batchs"] = batchs.count()
            type = TypeBudget.objects.get(id=budget['type'])
            budget["name_contract"] = contract.name
            budget['type'] = TypeBudgetSerializer(type).data
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)

    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = Budget.objects.all()
        ppto = self.get_object()
        serializer = self.serializer_class(ppto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_ppto = serializer.data
            return JsonResponse({"status_text": "Budget editado con exito.", "budget": data_ppto,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400) 
    
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
            budget_data = serializer.data
            response = {'budget': budget_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)