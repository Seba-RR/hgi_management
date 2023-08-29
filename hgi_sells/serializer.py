
from hgi_sells.models import Budget, PurchaseOrder, ProductOC, TypeOC, UnitProduct, Batch, Resource, ProdResource, CajaChica, EstadoCajaChica, ItemCajaChica, TypeDocument, ItemResource
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer


class TypeOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOC
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    total_oc = serializers.SerializerMethodField()
    n_products = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
    
    def get_total_oc(self, instance):
        total = 0
        if instance.type != 13:
            products = ProductOC.objects.filter(oc=instance.id)
            for product in products:
                total += product.price * product.amount
        else:
            total = instance.total
        return total

    def get_n_products(self, instance):
        products = ProductOC.objects.filter(oc=instance.id)
        return products.count()


class UnitProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitProduct
        fields = '__all__'

    
class ProductOCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOC
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


class ProdResourceSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()
    n_items = serializers.SerializerMethodField()
    contratado = serializers.SerializerMethodField()
    suma_total = serializers.SerializerMethodField()

    class Meta:
        model = ProdResource
        fields = '__all__'

    def get_disponible(self, instance):
        ingresado = 0
        items = ItemResource.objects.filter(resource = instance.id)
        for item in items:
            ingresado += item.total_price()
        total = instance.total - ingresado
        return total

    def get_n_items(self, instance):
        return (ItemResource.objects.filter(resource=instance.id)).count()
    
    def get_contratado(self, instance):
        products = ItemResource.objects.filter(batch=instance.batch.id).filter(resource=instance.resource.id)
        total_contratado = 0
        for product in products:
            total_contratado += product.total_price()
        return total_contratado
    
    def get_suma_total(self, instance):
        products = ItemResource.objects.filter(resource=instance.resource.id)
        total = 0
        for product in products:
            total += product.total_price()
        return total



class BatchSerializer(serializers.ModelSerializer):
    prodresources = serializers.SerializerMethodField()
    contratado = serializers.SerializerMethodField()
    suma_total = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = '__all__'
    
    def get_prodresources(self, instance):
        products = ProdResource.objects.filter(batch=instance.id)
        return ProdResourceSerializer(products, many=True).data
    
    def get_contratado(self, instance):
        products = ProductOC.objects.filter(batch=instance.id).filter(oc__type__id=7)
        total_contratado = 0
        for product in products:
            total_contratado += product.total_price()
        return total_contratado

    def get_suma_total(self, instance):
        products = ProductOC.objects.filter(batch=instance.id)
        total = 0
        for product in products:
            total += product.total_price()
        return total


class ItemResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemResource
        fields = '__all__'


class EstadoCajaChicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstadoCajaChica
        fields = '__all__'


class CajaChicaSerializer(serializers.ModelSerializer):
    name_company = serializers.SerializerMethodField()

    class Meta:
        model = CajaChica
        fields = '__all__'

    def get_name_company(self, instance):
        if instance.company is not None:
            return instance.company.name
        else:
            return "Company Eliminada"
        
class TypeDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeDocument
        fields = '__all__'

    
class ItemCajaChicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCajaChica
        fields = '__all__'