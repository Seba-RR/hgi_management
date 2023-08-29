
from hgi_static.models import ChangeManagement
from hgi_static.models import PermissionContractUser
from hgi_sells.models import ProductOC
from hgi_sells.models import Budget, Batch
from hgi_static.models import Contract, BuildingSite, TypeBudget, ClasiContract, EstadoContract, OCState, Currency, TypeContract, TypePago
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer


class ContractSerializer(serializers.ModelSerializer):
    total_pro = serializers.SerializerMethodField()
    total_prm = serializers.SerializerMethodField()
    total_batchs = serializers.SerializerMethodField()
    n_batchs = serializers.SerializerMethodField()
    total_apu = serializers.SerializerMethodField()
    name_company = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = '__all__'
    
    def get_total_pro(self, instance):
        total = 0
        try:
            pres = Budget.objects.filter(contract=instance.id)
            for pre in pres:
                total += pre.pro * pre.type.operacion
        except Budget.DoesNotExist:
            return total
        return total

    def get_total_prm(self, instance):
        total = 0
        try:
            pres = Budget.objects.filter(contract=instance.id)
            for pre in pres:
                total += pre.prm * pre.type.operacion
        except Budget.DoesNotExist:
            return total
        return total
    
    def get_total_batchs(self, instance):
        total = 0 
        try:
            batchs = Batch.objects.filter(contract=instance.id)
            for batch in batchs:
                products = ProductOC.objects.filter(batch=batch)
                for product in products:
                    total += product.total_price()
        except Batch.DoesNotExist:
            return total
        return total

    def get_n_batchs(self, instance):
        try:
            batchs = Batch.objects.filter(contract=instance.id)
            return batchs.count()
        except Batch.DoesNotExist:
            return 0
    
    def get_total_apu(self, instance):
        total = 0
        try:
            products = ProductOC.objects.filter(batch__contract=instance.id)
            for product in products:
                total += product.total_price()
        except ProductOC.DoesNotExist:
            return total
        return total
        
    def get_name_company(self, instance):
        if instance.company is not None:
            return instance.company.name
        else:
            return "Company Eliminada"

class BuildingSiteSerializer(serializers.ModelSerializer):
    name_company = serializers.SerializerMethodField()

    class Meta:
        model = BuildingSite
        fields = '__all__'
    
    def get_name_company(self, instance):
        if instance.company is not None:
            return instance.company.name
        else:
            return "Company Eliminada"
    

class TypeBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeBudget
        fields = '__all__'


class ClasiContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasiContract
        fields = '__all__'


class TypeContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeContract
        fields = '__all__'


class EstadoContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoContract
        fields = '__all__'


class TypePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePago
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

        
class OCStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCState
        fields = '__all__'


class PermissionContractUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionContractUser
        fields = '__all__'


class ChangeManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeManagement
        fields = '__all__'