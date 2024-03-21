import base64

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from django.views.decorators.cache import cache_page, never_cache

from ..serializer import *
from rest_framework import viewsets, status
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

class UpdatePassViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        answers = {'success': 0, 'user': {}}

        id = request.data.get('id', False)
        password = request.data.get('password', False)

        if id and password:
            user_info = User.objects.get(pk=id)
            user_info.set_password(password)
            user_info.save()

            if user_info is not None:
                answers['success'] = 1
                answers['user']['id'] = user_info.id
                answers['user']['username'] = user_info.username
                answers['user']['email'] = user_info.email
                answers['user']['first_name'] = user_info.first_name
                answers['user']['last_name'] = user_info.last_name
                answers['msg'] = 'Success'

                send_mail = MailsOperation()
                send_mail.change_password_information(user_info)

                return JsonResponse(answers, status=status.HTTP_200_OK)

        return Response(answers, status=status.HTTP_409_CONFLICT)


@action(detail=True, methods=['get', 'post'])
@authentication_classes([])
@permission_classes([])
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    @method_decorator(never_cache)
    #@method_decorator(cache_page(60 * 15))
    def list(self, request):
        answers = {'success': 0}
        return JsonResponse(answers, status=status.HTTP_400_BAD_REQUEST)


    @csrf_exempt
    def create(self, request, *args, **kwargs):

        '''
        Filipex Auto
        grzybek.rafal@gmail.com
        '''

        #Qw32$@qW3
        #test@nordeno-logistic.pl

        request.data._mutable = True
        username = request.data.get('username', '').strip()
        username_clear = request.data['username'].strip()
        request.data['username'] = username_clear.replace(" ", "")
        request.data._mutable = False

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = self.perform_create(serializer)

            User.objects.filter(
                pk=serializer.data['id']
            ).update(is_active=False)

            User.objects.filter(
                pk=serializer.data['id']
            ).update(username=username)

            headers = self.get_success_headers(serializer.data)

            user_info = User.objects.get(pk=serializer.data['id'])

            user_info.set_password(request.data.get('password', ''))
            user_info.save()

            answers = {
                'id': user_info.id
            }


            return Response(answers, status=status.HTTP_201_CREATED, headers=headers)
        else:
            answers = {'data': serializer.data, 'errors': serializer.errors}
            return Response(answers, status=status.HTTP_409_CONFLICT)


@action(detail=True, methods=['get', 'post'])
@authentication_classes([])
@permission_classes([])
class CheckUserViewSet(viewsets.ViewSet):

    @csrf_exempt
    @method_decorator(never_cache)
    #@method_decorator(cache_page(60 * 15))
    def list(self, request):
        answers = {'success': 0}

        if request.method == "GET":
            email = request.GET.get('email', False)
            username = request.GET.get('username', False)

            if email:
                answers = {'success': 1, 'email': 1, 'info': 'Email jest wolny'}
                try:
                    user = User.objects.get(email=email)
                    if user:
                        answers = {'success': 0, 'email': 0, 'info': 'Email jest już zajęty'}
                        return JsonResponse(answers, status=status.HTTP_200_OK)
                except Exception as e:
                    #print(e)
                    return JsonResponse(answers, status=status.HTTP_200_OK)

            if username:
                answers = {'success': 1, 'username': 1, 'info': 'Login jest wolny'}
                try:
                    user = User.objects.get(username=username)
                    if user:
                        answers = {'success': 10, 'username': 0, 'info': 'Login jest już zajęty'}

                    return JsonResponse(answers, status=status.HTTP_200_OK)
                except Exception as e:
                    return JsonResponse(answers, status=status.HTTP_200_OK)

        return JsonResponse(answers, status=status.HTTP_400_BAD_REQUEST)

