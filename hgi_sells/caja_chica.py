
from hgi2.utils import get_user_from_usertoken
from hgi_static.models import Contract, OCState, Currency, TypePago
from hgi_users.models import User
from hgi_sells.models import TypeOC
from hgi_sells.serializer import PurchaseOrderSerializer
from hgi_users.models import Supplier
from hgi_sells.models import PurchaseOrder
from hgi_sells.models import CajaChica
from hgi_sells.serializer import CajaChicaSerializer
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

class CajaChicaViewSet(viewsets.ModelViewSet):
    queryset = CajaChica.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = CajaChicaSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = CajaChica.objects.all()
        caja = self.get_object()
        data_caja = self.serializer_class(caja).data
        data_caja['name_state'] = caja.state.state
        data_caja['name_creator'] = caja.creator.short_name()
        data_caja['name_contract'] = caja.contract.name
        return JsonResponse({"caja_chica":data_caja}, status=200)
    
    def get_queryset(self):
        queryset = CajaChica.objects.all()
        cajas = queryset

        if 'contract' in self.request.query_params.keys():
            contract = self.request.query_params['contract']
            cajas = cajas.filter(contract = contract)
        
        if 'oc' in self.request.query_params.keys():
            oc = self.request.query_params['oc']
            cajas = cajas.filter(oc = oc)
            
        if 'company' in self.request.query_params.keys():
            company = self.request.query_params['company']
            cajas = cajas.filter(company = company)

        return cajas

    def list(self, request):
        user = get_user_from_usertoken(request.headers["Authorization"])
        cajas = self.get_queryset()
        if user.company is not None:
            cajas = cajas.filter(company=user.company)
        pages = Paginator(cajas.order_by('date_now').reverse(), 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        cajas_all = pages.page(out_pag).object_list
        serializer = self.serializer_class(cajas_all, many=True)
        response_data = serializer.data
        for caja_data in response_data:
            caja = CajaChica.objects.get(id=caja_data['id'])
            caja_data['name_state'] = caja.state.state
            caja_data['name_creator'] = caja.creator.short_name()
            caja_data['name_contract'] = caja.contract.name
        return JsonResponse({'total_pages': total_pages, 'total_objects':count_objects, 'actual_page': out_pag, 'objects': response_data}, status=200)

    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = CajaChica.objects.all()
        caja = self.get_object()
        if caja.state.id == 1 or caja.state.id == 6:
            if 'revision' in request.data.keys():
                del request.data['revision']
                data = request.data
                data['state'] = 2
                serializer = self.serializer_class(caja, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data_caja = serializer.data
                    supplier = Supplier.objects.get(rs = 'Constructora VDZ SpA')
                    state_oc = OCState.objects.get(id=6)
                    form_payment = TypePago.objects.get(id=1)
                    type_oc = TypeOC.objects.get(id=13)
                    currency = Currency.objects.get(id=1)
                    contract_oc = Contract.objects.get(id=data_caja['contract'])
                    transmitter_oc = User.objects.get(id=data_caja['creator'])
                    creator_oc = User.objects.get(id=data_caja['creator'])
                    caja_oc = PurchaseOrder.objects.create(
                        description='Generado por Caja Chica Id: ' + str(data_caja['id']),
                        supplier=supplier,
                        state=state_oc,
                        form_payment=form_payment,
                        contract=contract_oc,
                        transmitter=transmitter_oc,
                        creator=creator_oc,
                        type=type_oc,
                        currency=currency,
                        total=data_caja['total']
                    )
                    caja_oc_data = PurchaseOrderSerializer(caja_oc).data
                    caja.oc = caja_oc
                    caja.save()
                    return JsonResponse({"status_text": "Caja editada con exito.", "caja": data_caja,"oc":caja_oc_data},status=202)
                else:
                    return JsonResponse({"status_text": str(serializer.errors)}, status=400)
            else:
                serializer = self.serializer_class(caja, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data_caja = serializer.data
                    return JsonResponse({"status_text": "Caja editada con exito.", "caja": data_caja,},status=202)
                else:
                    return JsonResponse({"status_text": str(serializer.errors)}, status=400)
        else:
            return JsonResponse({"status_text": "Ya no puedes editarla."}, status=400)
        
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
            
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            item_cch_serializer = serializer.data
            return JsonResponse({"item_cch":item_cch_serializer}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)
        