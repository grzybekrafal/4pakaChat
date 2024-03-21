import random
import string

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import base64

from django.views.decorators.cache import cache_page, never_cache
from users.models import UsersPermision, UserRegeneratePassword


@action(detail=True, methods=['get', 'post'])
@authentication_classes([])
@permission_classes([])
class activate_user(viewsets.ViewSet):

    @method_decorator(never_cache)
    #@method_decorator(cache_page(60 * 15))
    @csrf_exempt
    def list(self, request):
        answers = {'success': 0, 'user': {}}

    @csrf_exempt
    def post(self, request):
        answers = {'success': 0, 'user': {}}

        if request.method == "POST":
            email = request.POST.get('email', False)
            token = request.POST.get('token', False)

            if email and token:
                user_permission = UsersPermision.objects.filter(user__email=email).filter(token_for_activate=token).first()

                if user_permission:
                    user_permission.token_is_used = True
                    user_permission.save()

                    User.objects.filter(
                        pk=user_permission.user.id
                    ).update(is_active=True)
                    answers = {'success': 1, 'user': {}}
                    return JsonResponse(answers, status=status.HTTP_200_OK)

        return JsonResponse(answers, status=status.HTTP_200_OK)

@action(detail=True, methods=['get', 'post'])
@authentication_classes([])
@permission_classes([])
class authentication_rest(viewsets.ViewSet):

    @csrf_exempt
    @method_decorator(never_cache)
    #@method_decorator(cache_page(60 * 15))
    def list(self, request):
        answers = {'success': 0, 'user': {}}
        return JsonResponse(answers, status=status.HTTP_400_BAD_REQUEST)


    @csrf_exempt
    def post(self, request):
        answers = {'success': 0, 'user': {}}

        if request.method == "POST":
            email = request.POST.get('username', False)
            password = request.POST.get('password', False)

            if email and password:
                #testUser = get_object_or_404(User, email=email)
                testUser = User.objects.filter(Q(email=email) | Q(username=email)).first()
                if testUser is not None:
                    user = authenticate(username=testUser.username, password=password)

                    if user is not None:
                        answers['success'] = 1
                        answers['user']['id'] = user.id
                        answers['user']['username'] = user.username
                        answers['user']['email'] = user.email
                        answers['user']['first_name'] = user.first_name
                        answers['user']['last_name'] = user.last_name

                        answers['msg'] = 'Success'
                        return JsonResponse(answers, status=status.HTTP_200_OK)

        answers['msg'] = 'Error validating the form !!'
        return JsonResponse(answers, status=status.HTTP_200_OK)
