import random
import string

from django.contrib.auth import get_user_model, login,logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, LoginForm
from .models import Captcha
# from django.contrib.auth.models import User
User = get_user_model()


@require_http_methods(['GET', 'POST'])
def zllogin(request):
    if request.method == 'GET':
        print('get')
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print("用户名或密码错误")
                # form.add_error('password', '用户名或密码错误')
                # return render(request, 'login.html', {'form': form})
                return redirect(reverse('blogauth:login'))


@require_http_methods(['POST', 'GET'])
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 注册用户
            user = User.objects.create_user(username=username, email=email, password=password)
            # 登录用户
            return redirect(reverse('blogauth:login'))
        else:
            return redirect(reverse('blogauth:register'))
            # return render(request,'register.html', {'form': form})
    else:
        return render(request, 'register.html')


def send_email_captcha(request):
    email = request.GET.get('email')
    print(email)
    if not email:
        return JsonResponse({
            "code": 400,
            "message": "Email is required"
        })
    # 生成验证码

    captcha = "".join(random.sample(string.digits, 4))
    # 存储验证码
    Captcha.objects.update_or_create(email=email, defaults={"captcha": captcha})
    # 发送验证码
    send_mail('博客注册验证码', message=f"您的验证码为：{captcha}", recipient_list=[email], from_email=None)

    return JsonResponse({
        "code": 200,
        "message": "验证码发送成功"
    })


def zllogout(request):
        logout(request)
        return redirect('/')
