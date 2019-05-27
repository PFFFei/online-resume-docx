from django.db import models
from django.conf import settings
import uuid
import os

User = settings.AUTH_USER_MODEL

'''
    自定义上传文件的存储路径
'''
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    # 随机字符对文件进行重命名
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    sub_folder = 'templates/file'
    if ext.lower() in ["jpg", "png"]:
        sub_folder = "templates/images"
    return os.path.join(sub_folder, filename)
'''
    管理员上传模板图片以及文件信息
'''
class Template(models.Model):
    KIND_CHOICES = (
        (0,'计算机'),
        (1,'法律'),
        (2,'医学'),
        (3,'金融学'),
    )

    title = models.CharField('模板标题', max_length=50)
    kind = models.SmallIntegerField('种类',choices=KIND_CHOICES,default=0)
    image = models.ImageField('模板图片',upload_to=user_directory_path)
    file = models.FileField('模板文件',upload_to=user_directory_path)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='模板信息'
        verbose_name_plural = verbose_name
'''
    用户简历信息
'''
class Resume(models.Model):
    title = models.CharField('简历标题', max_length=100)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    file = models.FileField('模板文件',upload_to=user_directory_path,blank=True)
    template = models.ForeignKey(Template, related_name='template', on_delete=models.CASCADE) # related_name 用来进行反向查询
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='简历信息'
        verbose_name_plural = verbose_name