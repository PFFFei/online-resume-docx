from django.urls import path,re_path 
from . import views 

app_name = 'resume'

urlpatterns = [
	# 模板列表 简历列表
	path('templates/',views.templates,name='templates'),
	path('list/',views.resume_list,name='list'),
	# 创建 删除
	re_path(r'^create/(?P<pk>\d+)/$',views.create_resume,name='create'),
	re_path(r'^delete/(?P<pk>\d+)/$',views.delete_resume,name='delete'),
]