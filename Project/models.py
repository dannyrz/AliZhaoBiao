from django.db import models
import Organization;
import time;

# Create your models here.
class Info(models.Model):
    IID = models.CharField('IID', unique=True, max_length=32)
    Name = models.CharField('项目名称', max_length=100)
    SerialNumber = models.CharField('项目编号', max_length=100, blank=True)
    #建立单独的关联表增加兼容性
    #Organization = models.ForeignKey(Organization.models.Info, 'IID', blank=False,default=time.time())
    FromName = models.CharField("公司／个人名称",blank=False, max_length=100)
    Address = models.CharField('项目地点', max_length=200, blank=True)
    BuildDimensions=models.FloatField('建筑面积',default=0)
    Country = models.CharField('国家', max_length=200, blank=True)
    Province = models.CharField('省份', max_length=50, blank=True)
    City = models.CharField('城市', max_length=50, blank=True)
    District = models.CharField('区域', max_length=50, blank=True)
    Abstract= models.TextField('项目概述', max_length=2000, blank=True)
    DocumentURL= models.FileField('相关文件',upload_to='upload',blank=True)
    Status_choices = (
        (0, "发布公告"),
        (1, "招标中"),
        (-1, "取消"),
    )
    Status = models.IntegerField('状态', choices=Status_choices, default=1)
