from django.urls import path

from . import views

app_name = 'blogauth'

urlpatterns = [
    path('login', views.zllogin, name='zllogin'),
    path('register', views.register, name='register'),
    path('captcha',views.send_email_captcha,name='captcha'),
    path('logout', views.zllogout, name='zllogout'),
]
