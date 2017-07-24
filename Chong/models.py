from django.db import models



# Create your models here.
class Task(models.Model):
    IID = models.CharField('IID', unique=True, blank=False, max_length=32)
    Name = models.CharField('任务名称', max_length=100, blank=False)
    CategoryID=models.CharField('类别', max_length=100, blank=True)
    SpiderName = models.CharField('爬虫名称', default='', max_length=100, blank=False)
    Charset_choices = (
        ("UTF-8","UTF-8"),
        ("GB2312","GB2312"),
    )
    Charset = models.CharField('编码', max_length=10,choices=Charset_choices, default="UTF-8")
    NeedLogin=models.BooleanField('需要登陆',default=0)
    Account=models.CharField('账号,密码', max_length=100, blank=True)
    WorkInterval = models.IntegerField('间隔时(min)', default=1)
    ThreadNumber = models.IntegerField('线程数', default=1)
    DataPersistenceType_choices = (
        ("WPRPC", "WordPress xmlrpc"),
        ("POST", "POST提交保存"),
        ("MYSQL", "MYSQL保存"),
    )
    DataPersistenceType = models.CharField('保存方式', max_length=10,choices=DataPersistenceType_choices, default="POST")
    WPUserName=models.CharField('WP账号', max_length=200, blank=True)
    WPPassword = models.CharField('WP密码', max_length=200, blank=True)
    PostURL = models.CharField('POST／RPC URL', max_length=200, blank=True)
    DatabaseConnectStr = models.CharField('数据库连接', max_length=5000, blank=True)

    StartURL=models.TextField('起始页', default='',max_length=5000, blank=True)

    ListURLRegularExpression = models.CharField('分页列表链接规则', max_length=100, blank=True)
    PageListRegularExpression = models.CharField('详情页列表规则', max_length=100, blank=True,default='')
    PageURLRegularExpression = models.CharField('详情页链接规则', max_length=100, blank=True, default='')

    PagePropertyRegularExpression = models.TextField('属性内容匹配', max_length=500, blank=False)
    ResponseFormat_choices = (
        ("XML", "HTML/XML"),
        ("JSON", "JSON"),
    )
    ResponseFormat = models.CharField('返回格式', choices=ResponseFormat_choices, max_length=10,default="XML")
    BodyFilterTextRegularExpression= models.CharField('正文过滤规则', max_length=5000, blank=False)
    TextReplace= models.CharField('替换文本', max_length=5000, blank=False)
    DownLoadImg_choices = (
        (0, "不下载"),
        (1, "下载"),
    )
    DownLoadImg = models.IntegerField('下载图片', choices=DownLoadImg_choices, default=0)
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


