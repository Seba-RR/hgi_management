from datetime import datetime
from django.db import models
from hgi_users.models import Company

from hgi_users.models import Client, User
from django.contrib.postgres.fields import ArrayField

"""
class Banco(models.Model):

    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=50, null=True, blank=True)
"""
class EstadoBuildingSite(models.Model):

    name = models.CharField(max_length=20, null=False)


class BuildingSite(models.Model):

    code = models.CharField(max_length=6, null=False)
    name = models.CharField(max_length=50, null=False)
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    #state = models.ForeignKey(EstadoBuildingSite, on_delete=models.CASCADE, null=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    date_now = models.DateTimeField(auto_now_add=True, null=True)



class ClasiContract(models.Model):

    name = models.CharField(max_length=20, null=False)
    abbreviation = models.CharField(max_length=5, null=True)


class TypeContract(models.Model):

    name = models.CharField(max_length=20, null=False)
    abbreviation = models.CharField(max_length=5, null=True)


class EstadoContract(models.Model):

    name = models.CharField(max_length=20, null=False)
    abbreviation = models.CharField(max_length=5, null=True)


class Contract(models.Model):

    code = models.CharField(max_length=9, null=False)
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    active =  models.BooleanField(default=True)

    par = models.BooleanField(default=False) #cargo por batch
    mat = models.BooleanField(default=False) #cargo por resource
    mau = models.IntegerField(default=0) #autorization oc
    auo = models.BooleanField(default=False) #autorizar dcs de building_site, no aplica (doctos = factura)
    proa = models.BooleanField(default=False) #controlar disponible
    oc = models.BooleanField(default=False) #oc obligatorio (factura) doctos con oc
    vis = models.BooleanField(default=False) #visado doctos (factura)
    uf = models.FloatField(null=False)
    sa = models.IntegerField(default=0) #controla sa (no aun)
    m2 = models.IntegerField(null=True) #dato
    peso = models.IntegerField(null=True) #dato
    ccp = models.BooleanField(default=False)
    
    state = models.ForeignKey(EstadoContract, on_delete=models.CASCADE, null=False)
    type = models.ForeignKey(TypeContract, on_delete=models.CASCADE, null=False, default=6) 
    classification = models.ForeignKey(ClasiContract, on_delete=models.CASCADE, null=False)
    building_site = models.ForeignKey(BuildingSite, on_delete=models.CASCADE, null=False)
    responsible = models.ForeignKey(User, related_name='user_responsible', on_delete=models.CASCADE, null=False)
    administrator = models.ForeignKey(User, related_name='user_administrator', on_delete=models.CASCADE, null=False)
    visitor = models.ForeignKey(User, related_name='user_visitor', on_delete=models.CASCADE, null=False)
    of_technique = models.ForeignKey(User, related_name='user_of_technique', on_delete=models.CASCADE, null=False)
    shopping = models.ForeignKey(User, related_name='user_shopping', on_delete=models.CASCADE, null=False)
    administrative = models.ForeignKey(User, related_name='user_administrative', on_delete=models.CASCADE, null=False)
    preventionist = models.ForeignKey(User, related_name='user_preventionist', on_delete=models.CASCADE, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    
    start = models.DateTimeField(auto_now_add=True, null=False)
    end = models.DateTimeField(null=True)
    

class TypeBudget(models.Model):

    description = models.CharField(max_length=30, null=False)
    diminutive = models.CharField(max_length=3, null=False)
    operacion = models.IntegerField(null=False)
    order = models.IntegerField(null=False)
    creator = models.ForeignKey(User, related_name='user', on_delete=models.SET_DEFAULT, default=1, null=False)


class TypePago(models.Model):

    description = models.CharField(max_length=50)
    days = models.IntegerField()
    order = models.IntegerField()

    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False) 


class Currency(models.Model):

    description = models.CharField(max_length=20, null=False)
    symbol = models.CharField(max_length=3, null=False)
    dec = models.IntegerField()


class OCState(models.Model):

    name = models.CharField(max_length=20, null=False)
    order = models.IntegerField()

class PermissionContractUser(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True)
    permissions = ArrayField(models.IntegerField(null=True), default=list)

class ChangeManagement(models.Model):
    model_choices = [
        ('Contract', 'Contract'),
        ('BuildingSite', 'BuildingSite'),
        ('Oc', 'OC'),
        ('Client', 'Client'),
        ('Supplier', 'Supplier'),
        ('CajaChica', 'CajaChica'),
        ('Budget', 'Budget'),
        ('ProdResource', 'ProdResource'),
        ('ItemCC', 'ItemCC'),
        ('ItemResource', 'ItemResource'),
        ('ProductOc', 'ProductOc'),
        ]
    
    type_model = models.CharField(max_length=20,choices=model_choices, null=True)
    obj_id = models.IntegerField()
    action = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False)
    date_now = models.DateTimeField(auto_now_add=True, null=False)