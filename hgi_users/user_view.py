from django.utils import timezone
from django.shortcuts import render
from hgi2.utils import get_user_from_usertoken
from hgi_users.serializer import CargoUserSerializer
from hgi_users.models import CargoUser
from hgi_users.serializer import UserSerializer
from hgi_users.models import User
from hgi_users.serializer import CreateUserSerializer, UserTokenSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    action,
)
from django.views.decorators.csrf import csrf_exempt
import json
from json.decoder import JSONDecodeError
from django.http.response import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = ()
    permission_classes = [permissions.AllowAny,]
    serializer_class = UserSerializer
    http_method_names = ["get", "patch", "delete"]


    def retrieve(self, request, pk):
        self.queryset = User.objects.all()
        #print(request.session['_auth_user_id'])
        user = self.get_object()
        data_user = self.serializer_class(user).data
        if user.position is not None:
            cargo_user = CargoUser.objects.get(id=user.position.id)
            cargo_user = CargoUserSerializer(cargo_user).data
            data_user["cargo"] = cargo_user
        return JsonResponse({"user":data_user}, status=200)

    def get_queryset(self):
        self.get_queryset = User.objects.all()
        users = self.queryset

        if 'company' in self.request.query_params.keys():
            company = self.request.query_params['company']
            users = users.filter(company = company)
        
        return users

    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = User.objects.all()
        user = self.get_object()
        edited = timezone.now()
        user.updated_at = edited
        user.save()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data_user = serializer.data
            return JsonResponse({"status_text": "Usuario editado con exito.", "user": data_user,},status=202)
        else:
            return JsonResponse({"status_text": str(serializer.errors)}, status=400)
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.id == 1 or user.is_superuser:
            return JsonResponse({"status_text": "No se puede eliminar este user."}, status=400)
        else:
            user.delete()
            return JsonResponse({"status_text": "Usuario eliminado."}, status=202)




@csrf_exempt
@api_view(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({"status_text": "Request error","error": str(error),},status=400,)
    token = request.headers["Authorization"]
    user = get_user_from_usertoken(token)
    if user.company is not None:
        data['company'] = user.company.id
    data["email"] = data["email"].lower()
    serializer = CreateUserSerializer(data=data)
    if serializer.is_valid():
        instance, token = serializer.save()
        data_user = serializer.data
        token = str(token).replace("(<Token: ", "").replace(">, True)", "")
        data_user["oauth_token"] = token
        data = {"token": token, "user": data_user["id"], "validation": True}
        validation_token = UserTokenSerializer(data=data)
        if validation_token.is_valid():
            validation_token.save()
            return JsonResponse({"status_text": "Usuario creado con exito.", "user": data_user,},status=202)
    return JsonResponse({"status_text": str(serializer.errors)}, status=400)


@csrf_exempt
@api_view(["POST"])
def login_v1(request):
    data = json.loads(request.body)
    if ("username" in data.keys()) and ("password" in data.keys()):
        user = User.objects.get(username=data["username"].lower())
        if user:
            if user.check_password(data["password"]):
                user = user
                serializer = UserSerializer(user)
                token = serializer.get_token()
                serializer = serializer.data
                serializer['token'] = str(token)
                return JsonResponse({"user":serializer}, status=202)
            return JsonResponse({"status_text": "Contraseña incorrecta"}, status=403)
        return JsonResponse({"status_text": "El user no existe"}, status=403)
    return JsonResponse({"status_text": "No se enviaron los parametros correctos"}, status=403)

@csrf_exempt
@api_view(["POST"])
def login_v2(request):
    data = json.loads(request.body)
    if ("username" in data.keys()) and ("password" in data.keys()):
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            user_data = UserSerializer(user).data
            if user.position is not None:
                cargo_user = CargoUser.objects.get(id=user.position.id)
                cargo_user = CargoUserSerializer(cargo_user).data
                user_data["cargo"] = cargo_user
            return JsonResponse({"user":user_data}, status=202)
        else:
            return JsonResponse({"status_text": "Contraseña incorrecta"}, status=403)
    return JsonResponse({"status_text": "No se envio la contraseña o username."}, status=403)


@csrf_exempt
@api_view(["POST"])
def logout_v1(request):
    #logout(request)
    return JsonResponse({"status_text" : "Sesión cerrada con exito."}, status=202)


@csrf_exempt
@api_view(["GET"])
def load_user(request):
    token = request.headers["Authorization"]
    user = get_user_from_usertoken(token)
    if user:
        serializer = UserSerializer(user)
        user_data = serializer.data
        user_data["token"] = token
        if user.position is not None:
            cargo_user = CargoUser.objects.get(id=user.position.id)
            cargo_user = CargoUserSerializer(cargo_user).data
            user_data["cargo"] = cargo_user

        response = {"status_code": 200, "user": user_data}
        return JsonResponse(response, status=200)
    return JsonResponse({"status_text": str(serializer.errors)}, status=400)