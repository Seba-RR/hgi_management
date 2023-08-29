from django.contrib.auth.models import AbstractUser
from django.db import models

class Company(models.Model):

    name = models.CharField(max_length=50, null=False)
    rut = models.CharField(max_length=15, null=False)
    code = models.CharField(max_length=20, null=True, blank=True)

    date_now_creado = models.DateTimeField(auto_now_add=True)

class PermissionContract(models.Model):

    name = models.CharField(max_length=50, null=False)
    ver_vb =  models.BooleanField(default=False)
    modify_vb = models.BooleanField(default=False)
    ver_contract = models.BooleanField(default=False)
    modify_contract = models.BooleanField(default=False)
    ver_ppto = models.BooleanField(default=False)
    modify_ppto = models.BooleanField(default=False)
    ver_oc = models.BooleanField(default=False)
    modify_oc = models.BooleanField(default=False)
    mano_building_site = models.BooleanField(default=False) #True if can see this type
    ver_cch = models.BooleanField(default=False)
    modify_cch = models.BooleanField(default=False)
    ver_ccr = models.BooleanField(default=False)
    modify_ccr = models.BooleanField(default=False)
    ver_ccp = models.BooleanField(default=False)
    modify_ccp = models.BooleanField(default=False)

class CargoUser(models.Model):
    
    name = models.CharField(max_length=50, null=False)
    por_contract = models.BooleanField(default=True)
    ver_oc = models.BooleanField(default=False)
    modify_oc = models.BooleanField(default=False)
    ver_vb = models.BooleanField(default=False)
    modify_vb = models.BooleanField(default=False)
    
    ver_contract = models.BooleanField(default=False)
    modify_contract = models.BooleanField(default=False)
    ver_ppto = models.BooleanField(default=False)
    modify_ppto = models.BooleanField(default=False)
    mano_building_site = models.BooleanField(default=False) #True if can see this type
    ver_cch = models.BooleanField(default=False)
    modify_cch = models.BooleanField(default=False)
    ver_ccr = models.BooleanField(default=False)
    modify_ccr = models.BooleanField(default=False)
    ver_ccp = models.BooleanField(default=False)
    modify_ccp = models.BooleanField(default=False)

class User(AbstractUser):
    type_choices = [
        ('Empleado', 'Empleado'),
        ('Usuario', 'Usuario'),
    ]
    username = models.CharField(max_length=30, null=True, unique=True)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=30)
    first_last_name = models.CharField(max_length=30, null=True)
    second_last_name = models.CharField(max_length=30, null=True)

    
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    rut = models.CharField(max_length=15, null=False)
    active = models.BooleanField(default=True)

    #Datos de empleado
    code = models.CharField(max_length=20, null=True, blank=True)
    position = models.ForeignKey(CargoUser, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def short_name(self):
        if self.first_last_name is not None:
            return self.first_name + " " + self.first_last_name
        else:
            return self.first_name
    
    def company_name(self):
        if self.company is not None:
            return self.company.name
        else:
            return "Company Eliminada"


class UserToken(models.Model):
    
    token = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    validation = models.BooleanField(default=False)
    recovery = models.BooleanField(default=False)


class Region(models.Model):
    name = models.CharField(max_length=60, default="")
    roman_number = models.CharField(max_length=5, default="")
    number = models.IntegerField(default=1)
    abbreviation = models.CharField(max_length=2, default="")
    
    class Meta:
        managed = True
        verbose_name = "Región"
        verbose_name_plural = "Regiones"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=60)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    class Meta:
        managed = True
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        order_with_respect_to = 'region'

    def __str__(self):
        return self.name


class Country(models.Model):

    name = models.CharField(max_length=80)
    iso = models.SmallIntegerField()
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)

    def __str__(self):
        return self.name



class Client(models.Model):
    country_choices = [('Chile', 'Chile'),
        ('Argentina', 'Argentina'),]

    business_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    code = models.CharField(max_length=3, null=True, blank=True)
    activity = models.CharField(max_length=100)
    rut = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=20,choices=country_choices, default='Chile',)
    active = models.BooleanField(default=True)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=20, default='Nombre Client')

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, blank=False)

    updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Supplier(models.Model):
    
    rut = models.CharField(max_length=20)
    rs = models.CharField(max_length=50)
    address = models.CharField(max_length=60)
    phone = models.CharField(max_length=10)
    web = models.CharField(max_length=25)
    contact = models.CharField(max_length=50)
    mail_contact = models.CharField(max_length=40)
    mail2_contact = models.CharField(max_length=40)
    name = models.CharField(max_length=50)
    credit = models.IntegerField()
    account = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    banco = models.CharField(max_length=20, null=True, blank=True)
    type_account = models.CharField(max_length=20, null=True, blank=True)

    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False, blank=False)
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, null=False, blank=False)
    date_now_creado = models.DateTimeField(auto_now_add=True)
    date_now_editado = models.DateTimeField(null=True, blank=True)