from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Template,Resume

admin.site.site_header = '在线简历系统'

class TemplateAdmin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('title','kind',)
    '''每页显示条目数'''
    list_per_page = 5
    '''设置可编辑字段'''
    list_editable = ('kind',)
    '''可搜索字段'''
    search_fields = ('title','kind',)

admin.site.register(Template,TemplateAdmin)

class ResumeAdmin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('title','user','template','created',)
    '''每页显示条目数'''
    list_per_page = 5
    '''按日期月份筛选'''
    date_hierarchy = 'created'
    '''按日期排序'''
    ordering = ('-created',)
    '''可搜索字段'''
    search_fields = ('title',)

admin.site.register(Resume, ResumeAdmin)

admin.site.unregister(Group)


