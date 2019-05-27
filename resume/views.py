from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.models import User
from resume.models import Resume,Template
from django.core.paginator import Paginator

from mailmerge import MailMerge

# 登陆装饰器,若为登陆则不能进行各种操作
@login_required
def templates(request):
    #  filter 为筛选
    template_0 = Template.objects.filter(kind=0)
    template_1 = Template.objects.filter(kind=1)
    template_2 = Template.objects.filter(kind=2)
    template_3 = Template.objects.filter(kind=3)
    return render(request,'resume/template_list.html',{'template_0':template_0,'template_1':template_1,'template_2':template_2,'template_3':template_3})

@login_required
def resume_list(request):
    user = get_object_or_404(User,id=request.user.id)
    resume_list = Resume.objects.filter(user=user).order_by('-created') # 按时间倒序排序
    if resume_list:
        # 实现分页功能
        paginator = Paginator(resume_list,5)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request,'resume/resume_list.html',{'page_obj':page_obj,'paginator':paginator,'is_paginated':True,})
    else:
        return render(request,'resume/resume_list.html')

@login_required
def create_resume(request,pk):
    user = get_object_or_404(User,id=request.user.id)
    template = Template.objects.get(pk=pk)
    # 将模板文件 与 信息 进行合并
    document = MailMerge(template.file)

    if request.method == 'POST':
        context =request.POST # 获取表单信息
        resume = Resume(user=user,template=template,title='{}-{}'.format(context['name'],context['purpose']))
        document.merge(
            name=context['name'],
            age=context['age'],
            experience=context['experience'],
            phone_no=context['phone_no'],
            email=context['email'],
            address=context['address'],
            purpose=context['purpose'],
            salary=context['salary'],
            institute_name=context['institute_name'],
            education_start_date=context['education_start_date'][:7],
            education_end_date=context['education_end_date'][:7],
            subject=context['subject'],
            academic=context['academic'],
            skill=context['skill'],
            company_name=context['company_name'],
            job_title=context['job_title'],
            job_start_date=context['job_start_date'][:7],
            job_end_date=context['job_end_date'][:7],
            job_description=context['job_description'],
            school_subject=context['school_subject'],
            school_job=context['school_job'],
            aboutme=context['aboutme'],
            )
        file = document.write("media\\resume\\{}-{}.docx".format(context['name'],context['purpose']))
        resume.file.name = "resume\\{}-{}.docx".format(context['name'],context['purpose'])
        resume.save()  # 保存到数据库
        # 提交表单后重定向到我的列表路由
        # reverse 为反向解析 即 resume:list 解析为 /list/
        # HttpResponseRedirect 会定向到 http://127.0.0.1/list/
        return HttpResponseRedirect(reverse("resume:list")) 
    else:
        return render(request,'resume/create.html')

@login_required
def delete_resume(request,pk):
    # 根据路由传来的 pk 值,从数据库中获取 并删除
    resume = get_object_or_404(Resume,pk=pk).delete()
    return HttpResponseRedirect(reverse("resume:list"))
