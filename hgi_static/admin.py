from django.contrib import admin
from hgi_static.models import PermissionContractUser
from hgi_static.models import Contract, BuildingSite, TypeBudget, ClasiContract, EstadoContract, OCState, Currency, TypeContract, TypePago, EstadoBuildingSite

class ContractAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "type", "start", "end"]
    class meta:
        model = Contract

class BuildingSiteAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "client", "creator"]
    class meta:
        model = BuildingSite

class TypeBudgetAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "operacion", "creator"]
    class meta:
        model = TypeBudget

class ClasiContractAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "abbreviation"]
    class meta:
        model = ClasiContract

class TypeContractAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "abbreviation"]
    class meta:
        model = TypeContract

class EstadoContractAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "abbreviation"]
    class meta:
        model = EstadoContract

class OCStateAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "order"]
    class meta:
        model = OCState

class EstadoBuildingSiteAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    class meta:
        model = EstadoBuildingSite

class PermissionContractUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "contract", "permissions"]
    class meta:
        model = PermissionContractUser


admin.site.register(Contract, ContractAdmin)
admin.site.register(BuildingSite, BuildingSiteAdmin)
admin.site.register(TypeBudget, TypeBudgetAdmin)
admin.site.register(ClasiContract, ClasiContractAdmin)
admin.site.register(TypeContract, TypeContractAdmin)
admin.site.register(EstadoContract, EstadoContractAdmin)
admin.site.register(TypePago)
admin.site.register(Currency)
admin.site.register(OCState, OCStateAdmin)
admin.site.register(EstadoBuildingSite, EstadoBuildingSiteAdmin)
admin.site.register(PermissionContractUser, PermissionContractUserAdmin)

