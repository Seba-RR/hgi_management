from django.db import models
from hgi_users.models import Company
from hgi_static.models import Contract, TypeBudget, TypePago, Currency, OCState
from hgi_users.models import User, Supplier


class Budget(models.Model):

    description = models.CharField(max_length=50, null=False)
    pre = models.IntegerField(null=False)
    prm = models.IntegerField(null=False)
    pro = models.IntegerField(null=False)
    ccp = models.CharField(max_length=10, null=False)

    type = models.ForeignKey(TypeBudget, on_delete=models.CASCADE, null=False)
    date_entrance = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False)


class TypeOC(models.Model):

    description = models.CharField(max_length=50, null=False)
    text = models.CharField(max_length=1000, null=False)
    code = models.IntegerField()
    sub = models.BooleanField(null=True, blank=True)
    rem = models.BooleanField(null=True, blank=True)
    pro = models.IntegerField(null=True, blank=True)
    pag = models.IntegerField(null=True, blank=True)
    arr = models.BooleanField(null=True, blank=True)
    rah = models.BooleanField(null=True, blank=True)
    cch = models.BooleanField(null=True, blank=True)
    man = models.BooleanField(null=True, blank=True)
    ope = models.IntegerField(null=True, blank=True)
    nco = models.CharField(max_length=3, null=True, blank=True)
    col = models.CharField(max_length=6, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)



class PurchaseOrder(models.Model):

    description = models.CharField(max_length=500, null=False)
    general_discount = models.IntegerField(default=0)
    observation = models.CharField(max_length=500, null=False, default="Sin Observaciones.")
    ref_oc = models.CharField(max_length=20, null=True)
    total = models.IntegerField(default=0)
    dispatch_address = models.CharField(max_length=60, null=True, blank=True) #parte del contract - editable
    
    ate_oc = models.CharField(max_length=50, null=True, blank=True) #parte del supplier
    mail = models.CharField(max_length=40, null=True, blank=True) #parte del supplier - editable
    mail2 = models.CharField(max_length=40, null=True, blank=True) #parte del supplier - editable

    autorization_adm = models.BooleanField(default=False) #user A
    autorization_res = models.BooleanField(default=False) #user R

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False)
    state = models.ForeignKey(OCState, on_delete=models.CASCADE, null=False, default=7) 
    form_payment = models.ForeignKey(TypePago, on_delete=models.CASCADE, null=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False)
    transmitter = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False, related_name="transmitter_oc")  # transmitter -> la necesita
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False, related_name="creator_oc") # quien la hizo
    type = models.ForeignKey(TypeOC, on_delete=models.CASCADE, null=False, default=6)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False)

    dispatch_date = models.DateTimeField(auto_now_add=True) # date_now creacion - editable
    date_now = models.DateTimeField(auto_now_add=True) # date_now creacion - editable


class UnitProduct(models.Model):

    name = models.CharField(max_length=10, null=False)
    time = models.CharField(max_length=5, null=True, blank=True)
    rfa = models.CharField(max_length=10, null=True, blank=True)


class Batch(models.Model):

    code = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=90, null=True, blank=True)
    total = models.IntegerField()

    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False)

    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)


class Resource(models.Model):

    code = models.CharField(max_length=5, null=False)
    description = models.CharField(max_length=50, null=False)
    chargeable = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    resource = models.ForeignKey('self', related_name="resource_padre", on_delete=models.CASCADE, null=True)


class ProdResource(models.Model):

    total = models.IntegerField()

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=False)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)


class ItemResource(models.Model):
    
    description = models.CharField(max_length=80, null=True, blank=True)
    sca = models.CharField(max_length=25, null=True, blank=True)
    unit = models.CharField(max_length=10, null=True, blank=True)
    amount = models.FloatField()
    price = models.IntegerField()
    observation = models.CharField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=False)
    ing = models.IntegerField(null=True)

    date_now = models.DateTimeField(auto_now_add=True)
    resource = models.ForeignKey(ProdResource, on_delete=models.CASCADE, null=False)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    
    def total_price(self):
        total = self.amount * self.price    
        return total


class ProductOC(models.Model):

    product = models.CharField(max_length=150, null=False)
    amount = models.FloatField()
    price = models.FloatField()
    discount = models.FloatField()
    mat = models.IntegerField(null=True, blank=True) # si tiene "batch" tiene mat -> material?
    afe = models.IntegerField(null=True, blank=True) 
    ing = models.IntegerField(null=True, blank=True) #ingreso?
    cpp = models.CharField(max_length=15, null=True, blank=True)
    lso = models.IntegerField(null=True, blank=True) #si no tiene ing tiene esto
    doc = models.IntegerField(null=True, blank=True) # 0
    car = models.IntegerField(null=True, blank=True) # 0
    moc = models.IntegerField(null=True, blank=True) # 0 
    ant = models.IntegerField(null=True, blank=True) # 0

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=False)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    unit = models.ForeignKey(UnitProduct, on_delete=models.CASCADE, null=False)
    oc = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=False)

    date_entrance = models.DateTimeField(auto_now_add=True)
    date_now_end = models.DateTimeField(null=True)

    def total_price(self):
        total = self.amount * self.price
        discount = (self.discount * total)/100        
        return (total - discount)


class EstadoCajaChica(models.Model):

    state = models.CharField(max_length=20, null=True, blank=True)
    date_now = models.DateTimeField(auto_now_add=True)
    oba = models.CharField(max_length=15, null=True, blank=True)

    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)


class CajaChica(models.Model):

    date_now = models.DateTimeField(auto_now_add=True) 
    aut = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True) #total de los products que contiene
    state = models.ForeignKey(EstadoCajaChica, on_delete=models.CASCADE, null=False, default=1)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    contract = models.ForeignKey(Contract, on_delete=models.SET_DEFAULT, default=1, null=False)
    oc = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)


class TypeDocument(models.Model):

    description = models.CharField(max_length=30, null=True, blank=True)
    operacion = models.IntegerField(null=True, blank=True)
    nco = models.CharField(max_length=3, null=True, blank=True)
    order_1 = models.IntegerField(null=True, blank=True)
    order_2 = models.IntegerField(null=True, blank=True)
    order_3 = models.IntegerField(null=True, blank=True)
    iva = models.BooleanField(default=True)
    ret = models.IntegerField(null=True, blank=True)
    reference = models.ForeignKey('self', related_name="doc_reference", on_delete=models.SET_NULL, null=True, blank=True)
    fim = models.CharField(max_length=2, null=True, blank=True)
    lve = models.IntegerField(null=True, blank=True)
    olv = models.IntegerField(null=True, blank=True)



class ItemCajaChica(models.Model):

    detail = models.CharField(max_length=70, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    total = models.IntegerField()
    ie = models.IntegerField(null=True, blank=True) #gasto en caso de petroleo - bencina
    number = models.IntegerField(null=True, blank=True)

    type = models.ForeignKey(TypeDocument, on_delete=models.CASCADE, null=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    caja_chica = models.ForeignKey(CajaChica, on_delete=models.CASCADE, null=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=False)

    date_now = models.DateTimeField(auto_now_add=True) 
