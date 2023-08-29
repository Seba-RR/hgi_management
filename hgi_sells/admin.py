from django.contrib import admin
from hgi_sells.models import Budget, PurchaseOrder, ProductOC, TypeOC, UnitProduct, Batch, Resource, ProdResource, CajaChica, EstadoCajaChica, ItemCajaChica, TypeDocument, ItemResource

class BudgetAdmin(admin.ModelAdmin):
    list_display = ["id","description", "prm", "pro", "type", "user", "contract"]
    class meta:
        model = Budget

class TypeOCAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "code", "user"]
    class meta:
        model = TypeOC

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ["id", "autorization_adm", "autorization_res", "state", "type", "creator", "transmitter"]
    class meta:
        model = PurchaseOrder

class UnitProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "time", "rfa"]
    class meta:
        model = UnitProduct

class ProductOCAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "amount", "price", "discount", "unit", "resource", "batch", "oc", "creator"]
    class meta:
        model = ProductOC

class BatchAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "total", "creator", "contract", "start", "end"]
    class meta:
        model = Batch

class ResourceAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "description", "chargeable", "resource"]
    class meta:
        model = Resource

class ProdResourceAdmin(admin.ModelAdmin):
    list_display = ["id", "total"]
    class meta:
        model = ProdResource

class ItemCajaChicaAdmin(admin.ModelAdmin):
    list_display = ["id", "detail", "total"]
    class meta:
        model = ItemCajaChica

class TypeDocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "operacion"]
    class meta:
        model = TypeDocument

class CajaChicaAdmin(admin.ModelAdmin):
    list_display = ["id", "total", "creator"]
    class meta:
        model = CajaChica

class EstadoCajaChicaAdmin(admin.ModelAdmin):
    list_display = ["id", "state", "creator"]
    class meta:
        model = EstadoCajaChica

class ItemResourceAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "amount", "price"]
    class meta:
        model = ItemResource


admin.site.register(Budget, BudgetAdmin)
admin.site.register(TypeOC, TypeOCAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(UnitProduct, UnitProductAdmin)
admin.site.register(ProductOC, ProductOCAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(ItemResource, ItemResourceAdmin)
admin.site.register(ProdResource, ProdResourceAdmin)
admin.site.register(ItemCajaChica, ItemCajaChicaAdmin)
admin.site.register(TypeDocument, TypeDocumentAdmin)
admin.site.register(CajaChica, CajaChicaAdmin)
admin.site.register(EstadoCajaChica, EstadoCajaChicaAdmin)