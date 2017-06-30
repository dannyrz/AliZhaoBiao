from django.db import models



# Create your models here.
class Task(models.Model):
    IID = models.CharField('IID', unique=True, blank=False, max_length=32)
    Name = models.CharField('任务名称', max_length=100, blank=False)
    Charset_choices = (
        ("UTF-8","UTF-8"),
        ("GB2312","GB2312"),
    )
    Charset = models.CharField('编码', max_length=10,choices=Charset_choices, default="UTF-8")
    WorkInterval = models.IntegerField('间隔时(min)', default=1)
    ThreadNumber = models.IntegerField('线程数', default=1)
    DatabaseConnectStr = models.CharField('数据库连接', max_length=5000, blank=False)
    InURLRegularExpression = models.CharField('入口列表页', max_length=100, blank=False)
    InURLNumber=models.IntegerField('页面数',default=1)
    PageProperty = models.CharField('属性名', max_length=100, blank=False)
    PagePropertyRegularExpression = models.CharField('属性内容匹配', max_length=100, blank=False)
    BodyFilterTextRegularExpression= models.CharField('属性名', max_length=5000, blank=False)
    TextReplace= models.CharField('替换文本', max_length=5000, blank=False)
    EnableBroswer_choices = (
        (0, "关闭"),
        (1, "启用"),
    )
    EnableBroswer = models.IntegerField('无头浏览器', choices=EnableBroswer_choices, default=0)
    Status_choices = (
        (0, "停止"),
        (1, "启用"),
    )
    Status = models.IntegerField('状态', choices=Status_choices, default=0)

