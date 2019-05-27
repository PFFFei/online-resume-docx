from django.urls import path 
from .views import login_view,register_view,logout_view,home

app_name = 'accounts'

urlpatterns = [
	# 主页 登陆 注册 退出
    path('',home,name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

]