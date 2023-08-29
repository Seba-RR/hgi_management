
from hgi2.utils import get_changes_list
from hgi2.utils import register_change
from hgi_sells.models import ProductOC
from hgi2.utils import add_info_oc
from hgi_static.serializer import ContractSerializer
from hgi_static.models import Contract
from hgi2.utils import get_user_from_usertoken, user_can_see_oc, can_accept_oc
from hgi_sells.models import PurchaseOrder
from hgi_sells.serializer import PurchaseOrderSerializer
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
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from itertools import chain

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = PurchaseOrderSerializer
    http_method_names = ["get", "patch", "delete", "post"]

    def retrieve(self, request, pk):
        self.queryset = PurchaseOrder.objects.all()
        oc = self.get_object()
        oc_data = self.serializer_class(oc).data
        add_info_oc(oc, oc_data)
        return JsonResponse({"order_compra":oc_data}, status=200)
    
    def get_queryset(self):
        self.get_queryset = PurchaseOrder.objects.all().order_by('-date_now')
        oc = self.queryset
        if 'supplier' in self.request.query_params.keys():
            supplier = self.request.query_params['supplier']
            oc = oc.filter(supplier = supplier)
        
        if 'creator' in self.request.query_params.keys():
            creator = self.request.query_params['creator']
            oc = oc.filter(creator = creator)
        
        if 'state' in self.request.query_params.keys():
            state = self.request.query_params['state']
            oc = oc.filter(state = state)
        
        if "search" in self.request.query_params.keys():
            product_query = Q(product__contains=self.request.query_params["search"])
            products = ProductOC.objects.filter(product_query)
            list_oc = []
            for product in products:
                if product.oc.id not in list_oc:
                    list_oc.append(product.oc.id)
            oc = oc.filter(id__overlap=[list_oc])

        return oc
    
    def list(self, request):

        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)
        ocs = self.get_queryset()
        final_oc_list = []
        if ocs.count() == 0:
            return JsonResponse ({"total_pages": 0,"total_objects": 0,"actual_page": 0,"objects": [],},status=200,)
        for oc in ocs.reverse():
            if user_can_see_oc(user, oc):
                final_oc_list.append(oc)

        pages = Paginator(final_oc_list, 99999)
        out_pag = 1
        total_pages = pages.num_pages
        count_objects = pages.count
        if self.request.query_params.keys():
            if "page" in self.request.query_params.keys():
                page_asked = int(self.request.query_params["page"])
                if page_asked in pages.page_range:
                    out_pag = page_asked
        oc_list = pages.page(out_pag).object_list
        serializer = self.serializer_class(oc_list, many=True)
        response_data = serializer.data
        for oc_data in response_data:
            oc = PurchaseOrder.objects.get(id = oc_data['id'])
            add_info_oc(oc, oc_data)

        return JsonResponse (
            {
                "total_pages": total_pages,
                "total_objects": count_objects,
                "actual_page": out_pag,
                "objects": response_data,
            },status=200,)
    
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
        if "transmitter" not in data.keys():
            data['transmitter'] = user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            oc_serializer = serializer.data
            register_change(oc_serializer["id"],[1,],user,"Oc")
            return JsonResponse({"oc":oc_serializer}, status=201)
        return JsonResponse({'status_text':str(serializer.errors)}, status=201)

    def partial_update(self, request, *args, **kwargs):
        
        if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
        else:
            return JsonResponse ({'status_text':'No usaste token'}, status=403)

        self.queryset = PurchaseOrder.objects.all()
        oc = self.get_object()
        contract = oc.contract
        can_accept, list_produtcs = can_accept_oc(oc)
        if 'auto_a' in request.data.keys() or 'auto_r' in request.data.keys():
            if (contract.administrator.id == user.id or contract.visitor == user.id) and contract.responsible.id == user.id:
                if can_accept:
                    serializer = PurchaseOrderSerializer(oc, data={"autorization_adm": True, "autorization_res": True, "state": 7}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        oc_data = serializer.data
                        register_change(oc_data["id"],[11,12,],user,"Oc")
                        return Response({'oc_data':serializer.data,'products':list_produtcs}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse ({'status_text':'La batch no acepta ese gasto.','products':list_produtcs}, status=403)
        if 'auto_a' in request.data.keys():
            if contract.administrator.id == user.id or contract.visitor == user.id:
                if can_accept:
                    if oc.autorization_res:
                        serializer = PurchaseOrderSerializer(oc, data={"autorization_adm": True, "state": 7}, partial=True)
                        accepted = True
                    else:
                        serializer = PurchaseOrderSerializer(oc, data={"autorization_adm": True}, partial=True)
                        accepted = False
                    if serializer.is_valid():
                        serializer.save()
                        oc_data = serializer.data
                        register_change(oc_data["id"],[11,],user,"Oc")
                        oc_data = serializer.data
                        return Response({'oc_data':oc_data,'products':list_produtcs}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse ({'status_text':'La batch no acepta ese gasto.','products':list_produtcs}, status=403)
            else:
                return JsonResponse ({'status_text':'No tienes autorización para realizar esta acción.'}, status=403)
        elif 'auto_r' in request.data.keys():
            if contract.responsible.id == user.id:
                if can_accept:
                    if oc.autorization_adm:
                        serializer = PurchaseOrderSerializer(oc, data={"autorization_res": True, "state": 7}, partial=True)
                        accepted = True
                    else:
                        serializer = PurchaseOrderSerializer(oc, data={"autorization_res": True}, partial=True)
                        accepted = False
                    if serializer.is_valid():
                        serializer.save()
                        oc_data = serializer.data
                        register_change(oc_data["id"],[12,],user,"Oc")
                        oc_data = serializer.data
                        return Response({'oc_data':oc_data,'products':list_produtcs}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse ({'status_text':'La batch no acepta ese gasto.','products':list_produtcs}, status=403)
            else:
                return JsonResponse ({'status_text':'No tienes autorización para realizar esta acción.'}, status=403)
        else:
            changes = get_changes_list(request.data)
            serializer = PurchaseOrderSerializer(oc, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                oc_data = serializer.data
                register_change(oc_data["id"],changes,user,"Oc")
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

@csrf_exempt
@api_view(["GET"])
def oc_por_autorizar(request):
    if 'Authorization' in request.headers:
            user = get_user_from_usertoken(request.headers['Authorization'])
    else:
        return JsonResponse ({'status_text':'No usaste token'}, status=403)
    oc_adm = PurchaseOrder.objects.filter(contract__administrator__id=user.id).filter(autorization_adm=False)
    oc_res = PurchaseOrder.objects.filter(Q(contract__responsible__id=user.id) | Q(contract__visitor__id=user.id)).filter(autorization_res=False)
    model_combination = list(chain(oc_adm, oc_res))
    oc_list = list(set(model_combination))
    oc_list_data = PurchaseOrderSerializer(oc_list, many=True).data
    return JsonResponse ({'status_text':'OC por autorizar', 'oc':oc_list_data}, status=200)

