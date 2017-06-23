from django.db import models
import Organization;
# Create your models here.
class Base(models.Model):
    IID = models.CharField('IID', max_length=32)
    Name = models.CharField('机构名称', max_length=200)
    OrganizationID = models.ForeignKey(Organization.Base, 'IID', blank=True)
    Address = models.CharField('地址', max_length=200, blank=True)
    Country = models.CharField('国家', max_length=200, blank=True)
    Province = models.CharField('省份', max_length=50, blank=True)
    City = models.CharField('城市', max_length=50, blank=True)
    District = models.CharField('区域', max_length=50, blank=True)  # 区
