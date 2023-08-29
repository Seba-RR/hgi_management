 
from hgi_users.models import User
from hgi2.utils import register_change, get_changes_list, create_contract_user_permission, get_user_from_usertoken
from hgi_sells.serializer import BudgetSerializer
from hgi_sells.models import Budget
from hgi_static.models import Contract, EstadoContract, BuildingSite
from hgi_static.serializer import ContractSerializer
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



class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = ContractSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = Contract.objects.all()
        contract = self.get_object()
        data_contract = self.serializer_class(contract).data
        ppto = Budget.objects.filter(contract=data_contract['id'])
        data_contract['budgets'] = BudgetSerializer(ppto, many=True).data
        status = EstadoContract.objects.get(id=data_contract['state'])
        building_site = BuildingSite.objects.get(id=data_contract['building_site'])
        data_contract['state_name'] = status.name
        data_contract['building_site_name'] = building_site.name
        return JsonResponse({"contract":data_contract}, status=200)
    
    def get_queryset(self):
        queryset = Contract.objects.all()
        contracts = queryset

        if 'company' in self.request.query_params.keys():
            company = self.request.query_params['company']
            contracts = contracts.filter(company = company)
        
        return contracts
    
    def list(self, request):
        user = get_user_from_usertoken(request.headers["Authorization"])
        contracts = self.get_queryset()
        if user.company is not None:
            contracts = contracts.filter(company=user.company)

        pages = Paginator(contracts.order_by('start').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        contracts_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(contracts_all, many=True)
        response_data = serializer.data
        for contract in response_data:
            status = EstadoContract.objects.get(id=contract['state'])
            building_site = BuildingSite.objects.get(id=contract['building_site'])
            contract['code_building_site'] = building_site.code
            contract['code_client'] = building_site.client.code
            contract['state_name'] = status.name
            contract['building_site_name'] = building_site.name
        
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
                data['company'] = user.company.id
            else:
                user_creator = User.objects.get(id=data['creator'])
                data['company'] = user_creator.company.id
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            contract_data = serializer.data
            register_change(contract_data["id"],[1,],user,"Contract")
            create_contract_user_permission(contract_data)
            response = {'contract': contract_data}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)
    
    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = Contract.objects.all()
        product = self.get_object()

        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        
        serializer = self.serializer_class(product, data=request.data, partial=True)
        changes = get_changes_list(request.data)
        if serializer.is_valid():
            serializer.save()
            contract_data = serializer.data
            register_change(contract_data["id"],changes,user,"Contract")
            return JsonResponse({"status_text": "Contract editado con exito.", "contract": contract_data,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400)
    
    def destroy(self, request, *args, **kwargs):
        self.queryset = Contract.objects.all()
        contract = self.get_object()
        if contract is not None:
            contract.delete()
            return JsonResponse({'status_text': 'Contract eliminado correctamente'}, status=200)