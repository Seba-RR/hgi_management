
from django.contrib import admin
from hgi_users.models import PermissionContract
from hgi_users.models import City, UserToken, Region, Client, User, Country, CargoUser, Supplier

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "phone_number", "code", "position"]
    class meta:
        model = User

class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "business_name", "address", "rut", "activity", "phone", "contact"]
    class meta:
        model = Client

class CargoUserAdmin(admin.ModelAdmin):
    list_display = ["name", "por_contract", "ver_oc", "modify_oc", "ver_vb", "modify_vb"]
    class meta:
        model = CargoUser

class SupplierAdmin(admin.ModelAdmin):
    list_display = ["id", "rut", "rs", "phone", "web", "creator"]
    class meta:
        model = Supplier

class PermissionContractAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "ver_vb", "modify_vb", "ver_contract", "modify_contract", "ver_ppto", "modify_ppto", "ver_oc", "modify_oc", "mano_building_site", "ver_cch", "modify_cch", "ver_ccr", "modify_ccr", "ver_ccp", "modify_ccp"]
    class meta:
        model = PermissionContract 

admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(UserToken)
admin.site.register(Country)
admin.site.register(CargoUser, CargoUserAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(PermissionContract, PermissionContractAdmin)
