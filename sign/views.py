from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
import uuid as uid

from sign.models import Users


def index(request):
    return render(request, 'main/main.html')

@csrf_exempt
@api_view(('GET', 'POST'))
def signIn(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        token = request.POST.get('token', '')

        user = Users.objects.filter(username=username).first()

        if user is None:
            data = dict(
                # msg='id 불일치',
                code='001'
            )
            return Response(data)
        else:
            users = Users.objects.get(username=username)
            if check_password(password, user.password):

                users.token = token
                users.save()

                user = dict(
                    id=str(user.id)
                )
                data = dict(
                    # msg='로그인 성공',
                    user=user,
                    code='000',
                )
                return Response(data=data)
            else:
                data = dict(
                    # msg='패스워드 불일치',
                    code='002'
                )
                return Response(data=data)
@csrf_exempt
@api_view(('GET', 'POST'))
def signUp(request):
    if request.method == "POST":
        id = uid.uuid4()
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        pw_crypted = make_password(password)

        if Users.objects.filter(username=username).exists():
            data = dict(
                # msg='이미 존재하는 아이디 입니다.',
                code='001'
            )
            return Response(data=data)
        else:

            Users.objects.create(id=id, username=username, password=pw_crypted, token="")
            data = dict(
                # msg='회원가입 성공,'
                code='000',
            )
            return Response(data=data)

    if request.method == "DELETE":
        return HttpResponse("withdraw")

    if request.method == "PUT":
        return HttpResponse("sign put")

