
from hgi_users.models import Company
from hgi_static.serializer import PermissionContractUserSerializer
from hgi_static.models import PermissionContractUser
from hgi_users.models import PermissionContract
from hgi_users.models import Country, City, Supplier, Region, Client, User, UserToken, CargoUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_flex_fields import FlexFieldsModelSerializer
from django.core.exceptions import ObjectDoesNotExist


class PermissionContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionContract
        fields = '__all__'

class CreateUserSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser', 'position',
                  'first_name', 'first_last_name', 'second_last_name','active',
                  'password', 'created_at', 'updated_at', 'phone_number', 'rut', 'code','company')
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


    def save(self, *args, **kwargs):
        instance = super(CreateUserSerializer, self).save(*args, **kwargs)
        token = Token.objects.get_or_create(user=self.instance)
        return instance, token

    def get_token(self):
        try:
            token = Token.objects.get(user=self.instance)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=self.instance)
        return token

    def new_token(self):
        Token.objects.filter(user=self.instance).delete()
   

class CargoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoUser
        fields = '__all__'


class UserSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True)
    permiso_contract = serializers.SerializerMethodField()
    name_company = serializers.SerializerMethodField()
    cargo_user = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser', 'position',
                  'first_name', 'first_last_name', 'second_last_name','active',
                  'password', 'created_at', 'updated_at', 'phone_number', 'rut', 'code', 'permiso_contract', 'name_company', 'cargo_user')
        read_only_fields = ('created_at', 'updated_at',)
    
    def get_token(self):
        try:
            token = Token.objects.get(user=self.instance)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=self.instance)
        return token
    
    def get_permiso_contract(self, instance):
        permissions = PermissionContractUser.objects.filter(user=instance.id)
        permissions = PermissionContractUserSerializer(permissions, many=True).data
        permiso_contract_user = {}
        for permiso in permissions:
            permiso_contract = {}
            for id_permiso in permiso["permissions"]:
                permiso_contract_data = PermissionContractSerializer(PermissionContract.objects.get(id=id_permiso)).data
                permiso_contract[permiso_contract_data["name"]] = permiso_contract_data
            permiso_contract_user[permiso["contract"]] = permiso_contract
        return permiso_contract_user

    def get_name_company(self, instance):
        if instance.company is not None:
            return instance.company.name
        else:
            return "Company Eliminada"
    
    def get_cargo_user(self, instance):
        if instance.position is not None:
            return CargoUserSerializer(instance.position).data
        else:
            return {}



class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ('user', 'token', 'validation', 'recovery')


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'business_name', 'address', 'commune', 'activity', 'rut','phone','country','active','contact','region','city','code','email',)
        read_only_fields = ('created_at', 'updated_at',)
    

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'