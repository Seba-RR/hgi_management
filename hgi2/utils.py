
from hgi_static.models import ChangeManagement
from hgi_users.models import User
from hgi_static.models import PermissionContractUser
from hgi_sells.serializer import BatchSerializer
from hgi_sells.models import Batch
from hgi_sells.models import ProductOC
from hgi_static.models import Contract
from hgi_users.models import CargoUser
from hgi_users.models import UserToken


def get_user_from_usertoken(token):
    token = token.replace("Token ", "")
    user = UserToken.objects.get(token=token).user
    return user

def user_can_see_oc(user, oc):
    cargo = CargoUser.objects.get(id=user.position.id)
    if cargo.ver_oc:
        return True
    elif cargo.por_contract:
        contract = oc.contract
        if user.id == contract.responsible.id or user.id == contract.administrator.id or user.id == contract.visitor.id or user.id == contract.of_technique.id or user.id == contract.shopping.id or user.id == contract.administrative.id or user.id == contract.preventionist.id:
            return True
    return False

def user_can_edit_oc(user, oc):
    cargo = CargoUser.objects.get(id=user.position.id)
    if cargo.modify_oc:
        return True
    elif cargo.por_contract:
        contract = oc.contract
        if user.id == contract.responsible.id or user.id == contract.administrator.id or user.id == contract.visitor.id or user.id == contract.of_technique.id or user.id == contract.shopping.id or user.id == contract.administrative.id or user.id == contract.preventionist.id:
            return True
    return False

def can_accept_oc(oc):
    part_dict = {}
    products = ProductOC.objects.filter(oc=oc)
    can = True
    for product in products:
        data = {}
        batch = product.batch
        if batch.id in part_dict.keys():
            data = part_dict[product.batch.id]
            data['total_oc'] += product.total_price()
            data['new_balance'] = data['balance'] - data['total_oc']
            part_dict[batch.id] = data
        else:
            products = ProductOC.objects.filter(batch=batch.id)
            batch_ingresado = 0
            for product in products:
                batch_ingresado += product.total_price()
            data['total_batch'] = batch.total
            data['total_used'] = batch_ingresado
            data['balance'] = batch.total - batch_ingresado
            data['total_oc'] = product.total_price()
            data['new_balance'] = data['balance'] - data['total_oc']
            part_dict[batch.id] = data
    for batch_data in part_dict:
        if batch_data['new_balance'] < 0:
            can = False
    return can, part_dict

 
def get_total_batchs_APU(batchs):
    batchs = BatchSerializer(batchs, many=True).data
    total_batchs = 0
    total_ingresado = 0
    for batch in batchs:
        total_batchs += batch['total']
        products = ProductOC.objects.filter(batch=batch['id'])
        for product in products:
            total_ingresado += product.total_price()
    return total_batchs, total_ingresado

def add_info_oc(oc, oc_data):

    oc_data['name_supplier'] = oc.supplier.rs
    oc_data['name_transmitter'] = oc.transmitter.short_name()
    oc_data['name_contract'] = oc.contract.name
    oc_data['name_state'] = oc.state.name
    oc_data['name_form_payment'] = oc.form_payment.description
    oc_data['name_type'] = oc.type.description
    oc_data['name_currency'] = oc.currency.symbol 
    return

def create_contract_user_permission(contract_data):
    permissions = {}
    contract = Contract.objects.get(id=contract_data['id'])

    if contract.responsible.id not in permissions.keys():
        permissions[contract.responsible.id] = [1,]
    else:
        permissions[contract.responsible.id].append(1)

    if contract.administrator.id not in permissions.keys():
        permissions[contract.administrator.id] = [3,]
    else:
        permissions[contract.administrator.id].append(3)

    if contract.visitor.id not in permissions.keys():
        permissions[contract.visitor.id] = [2,]
    else:
        permissions[contract.visitor.id].append(2)
    
    if contract.of_technique.id not in permissions.keys():
        permissions[contract.of_technique.id] = [6,]
    else:
        permissions[contract.of_technique.id].append(6)
    
    if contract.shopping.id not in permissions.keys():
        permissions[contract.shopping.id] = [5,]
    else:
        permissions[contract.shopping.id].append(5)

    if contract.administrative.id not in permissions.keys():
        permissions[contract.administrative.id] = [7,]
    else:
        permissions[contract.administrative.id].append(7)

    if contract.preventionist.id not in permissions.keys():
        permissions[contract.preventionist.id] = [4,]
    else:
        permissions[contract.preventionist.id].append(4)
     
    for key, permission in permissions.items():
        user = User.objects.get(id=key)
        PermissionContractUser.objects.create(user=user,contract=contract,permissions=permission)

    return

def get_changes_list(data):
    changes = []

    if "name" in data.keys():
        changes.append(2)
    if "business_name" in data.keys():
        changes.append(2)
    if "code" in data.keys():
        changes.append(3)
    if "code" in data.keys():
        changes.append(3)
    if "address" in data.keys():
        changes.append(4)
    if "address" in data.keys():
        changes.append(4)
    if "state" in data.keys():
        changes.append(5)
    if "type" in data.keys():
        changes.append(6)
    if "classification" in data.keys():
        changes.append(7)
    if "building_site" in data.keys():
        changes.append(8)
    if "description" in data.keys():
        changes.append(9)
    if "observation" in data.keys():
        changes.append(10)
    if "auto_a" in data.keys():
        changes.append(11)
    if "auto_r" in data.keys():
        changes.append(12)
    if "activity" in data.keys():
        changes.append(13)
    if "rut" in data.keys():
        changes.append(14)
    if "phone" in data.keys():
        changes.append(15)
    if "phone" in data.keys():
        changes.append(15)
    if "email" in data.keys():
        changes.append(16)
    if "mail_contact" in data.keys():
        changes.append(16)
    if "contact" in data.keys():
        changes.append(17)
    if "contact" in data.keys():
        changes.append(17)
    if "rs" in data.keys():
        changes.append(18)
    if "credit" in data.keys():
        changes.append(19)
    if "account" in data.keys():
        changes.append(20)
    if "banco" in data.keys():
        changes.append(21)
    return changes 

def register_change(id,change_types,user,changed_model):
    types = {
        1: "Objeto Creado",
        2: "Objeto Editado (Nombre)",
        3: "Objeto Editado (Código)",
        4: "Objeto Editado (Dirección)",
        5: "Objeto Editado (Estado)",
        6: "Objeto Editado (Type)",
        7: "Objeto Editado (Clasificación)",
        8: "Objeto Editado (BuildingSite)",
        9: "Objeto Editado (Glosa)",
        10: "Objeto Editado (Observación)",
        11: "Orden de Compra Autorizada (A)",
        12: "Orden de Compra Autorizada (R)",
        13: "Objeto Editado (Actividad)",
        14: "Objeto Editado (Rut)",
        15: "Objeto Editado (Teléfono)",
        16: "Objeto Editado (Email)",
        17: "Objeto Editado (Contacto)",
        18: "Objeto Editado (Razón Social)",
        19: "Objeto Editado (Crédito)",
        20: "Objeto Editado (Cuenta)",
        21: "Objeto Editado (Banco)",
    }
    for change_type in change_types:
        ChangeManagement.objects.create(type_model=changed_model, obj_id=id, action=types[change_type], user=user)
    
    return