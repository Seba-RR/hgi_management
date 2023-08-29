from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from hgi_sells import orden_compra_view
from hgi_sells.caja_chica import CajaChicaViewSet
from hgi_sells.estado_cchica import EstadoCajaChicaViewSet
from hgi_sells.item_cchica import ItemCajaChicaViewSet
from hgi_sells.item_recurso import ItemResourceViewSet
from hgi_sells.orden_compra_view import PurchaseOrderViewSet
from hgi_sells.partida_view import BatchViewSet
from hgi_sells.presupuesto_view import BudgetViewSet
from hgi_sells.prodrecurso_view import ProdResourceViewSet
from hgi_sells.producto_oc_view import ProductOCViewSet
from hgi_sells.recurso_view import ResourceViewSet
from hgi_sells.tipo_doc import TypeDocumentViewSet
from hgi_sells.tipooc_view import TypeOCViewSet
from hgi_sells.unidad_producto_view import UnitProductViewSet
from hgi_static.clasicontrato_view import ClasiContractViewSet
from hgi_static.contrato_view import ContractViewSet
from hgi_static.estado_contrato_view import EstadoContractViewSet
from hgi_static.estado_oc_view import OCStateViewSet
from hgi_static.moneda_view import CurrencyViewSet
from hgi_static.obra_view import BuildingSiteViewSet
from hgi_static.permiso_contrato_user_view import PermissionContractUserViewSet
from hgi_static.tipo_pago_view import TypePagoViewSet
from hgi_static.tipocontrato_view import TypeContractViewSet
from hgi_static.tipoppto_view import TypeBudgetViewSet
from hgi_users.cargo_user import CargoUserViewSet
from hgi_users.city_view import CityViewSet
from hgi_users.company_view import CompanyViewSet
from hgi_static.gestion_cambios_view import ChangeManagementViewSet
from hgi_users import client_view
from hgi_users import user_view
from hgi_users.country_view import CountryViewSet
from hgi_users.permiso_contrato_view import PermissionContractViewSet
from hgi_users.proveedor_view import SupplierViewSet
from hgi_users.region_view import RegionViewSet

from rest_framework import routers
from django.conf.urls import include

router = routers.SimpleRouter()
router.register(r"users", user_view.UserViewSet)
router.register(r"clients", client_view.ClientViewSet)
router.register(r"contracts", ContractViewSet)
router.register(r"type_pptos", TypeBudgetViewSet)
router.register(r"budget", BudgetViewSet)
router.register(r"building_sites", BuildingSiteViewSet)
router.register(r"type_oc", TypeOCViewSet)
router.register(r"order_compra", PurchaseOrderViewSet)
router.register(r"unit_product", UnitProductViewSet)
router.register(r"product_oc", ProductOCViewSet)
router.register(r"supplier", SupplierViewSet)
router.register(r"country", CountryViewSet)
router.register(r"region", RegionViewSet)
router.register(r"city", CityViewSet)
router.register(r"clasi_contract", ClasiContractViewSet)
router.register(r"type_contract", TypeContractViewSet)
router.register(r"state_contract", EstadoContractViewSet)
router.register(r"type_pago", TypePagoViewSet)
router.register(r"currency", CurrencyViewSet)
router.register(r"state_oc", OCStateViewSet)
router.register(r"batch", BatchViewSet)
router.register(r"cargo_user", CargoUserViewSet)
router.register(r"item_resource", ItemResourceViewSet)
router.register(r"resources", ResourceViewSet)
router.register(r"prod_resource", ProdResourceViewSet)
router.register(r"item_cch", ItemCajaChicaViewSet)
router.register(r"type_doc", TypeDocumentViewSet)
router.register(r"caja_chica", CajaChicaViewSet)
router.register(r"state_cch", EstadoCajaChicaViewSet)
router.register(r"permiso_cuser", PermissionContractUserViewSet)
router.register(r"permiso_contract", PermissionContractViewSet)
router.register(r"gestion_cambios", ChangeManagementViewSet)
router.register(r"company", CompanyViewSet)

slashless_router = routers.SimpleRouter(trailing_slash=False)
slashless_router.registry = router.registry[:]

urlpatterns = [
    
    re_path(r"^", include(router.urls)),
    path('admin/', admin.site.urls),
    path('create_user', user_view.register, name='register'),
    path('login', user_view.login_v1, name='login_v1'),
    path('login_v2', user_view.login_v2, name='login_v2'),
    path('logout', user_view.logout_v1, name='logout'),
    path('load_user', user_view.load_user, name='load_user'),
    
    #_____ Orden de Compra _____________
    path('oc_por_autorizar', orden_compra_view.oc_por_autorizar, name="oc_por_autorizar"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
