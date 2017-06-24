import time
from django.db import models


# Create your models here.
# 公司，团体，设计院，监理公司，企事业单位资料
class Type(models.Model):
    IID=models.CharField('IID',unique=True, max_length=32)
    Name= models.CharField('类型名称',max_length=200)
    Remark= models.CharField('备注',max_length=500)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = '单位类型'
        #app_label = "schedule"


# 公司，团体，设计院，监理公司，企事业单位资料
class Info(models.Model):
    IID=models.CharField('IID',max_length=32, unique=True, blank=False)
    Name = models.CharField('机构名称',max_length=200)
    CreditNumber = models.CharField('机构代码', max_length=32, blank=True)  # 证书 营业执照号 统一代码
    LegalRepresentative = models.CharField('法人代表',max_length=32,blank=True) #法人代表
    RegisteredCapital=models.IntegerField('注册资金',default=0) #注册资金
    BusinessScope =models.CharField('经营范围',max_length=200,blank=True) #经营范围
    FoundedDate= models.DateField('成立时间',default='1970-1-1')#成立时间
    BusinessTerm= models.DateField('经营期限',default='1970-1-1') # 经营期限
    LogoURL = models.ImageField('LOGO',upload_to='upload',blank=True)
    WebSiteURL = models.URLField('网站',max_length=200,blank=True) #网站
    Address= models.CharField('地址',max_length=200,blank=True)
    Country= models.CharField('国家',max_length=200,blank=True)
    Province= models.CharField('省份',max_length=50,blank=True)
    City = models.CharField('城市',max_length=50,blank=True)
    District = models.CharField('区域',max_length=50,blank=True)#区
    Location=models.CharField('经纬度',max_length=50,blank=True)#经纬度
    Contact= models.CharField('联系人',max_length=50,blank=True)#联系人
    EMail= models.CharField('电子邮件',max_length=100,blank=True)
    TelPhone = models.CharField('电话',max_length=20,blank=True)
    QQ= models.CharField('QQ',max_length=20,blank=True)
    WeiXin= models.CharField('微信',max_length=50,blank=True)
    WeiXinPublic= models.CharField('微信公众号',max_length=100,blank=True)
    WangWang= models.CharField('旺旺',max_length=50,blank=True)
    DingDing= models.CharField('钉钉',max_length=50,blank=True)
    ZipCode = models.CharField('邮编',max_length=10,blank=True)
    Profile = models.CharField('简介',max_length=2000,blank=True)#简介
    Grade=models.FloatField('评分',default=0) #评分
    Level=models.IntegerField('等级',default=0) #等级
    CreateTime = models.DateTimeField('创建时间', auto_now = True)#创建时间
    Type=models.ForeignKey(Type,'IID',blank=True)
    Status_choices = (
        (0, "待审核"),
        (1, "审核通过"),
        (-1, "审核未通过"),
    )
    Status = models.IntegerField('状态',choices=Status_choices, default=1)

    class Meta:
        verbose_name_plural = '单位基本资料'



# 组织资质
class Credential(models.Model):
    OrganizationID= models.CharField(max_length=32) #组织ID
    TypeID= models.CharField(max_length=32) #资质类别ID
    PicUrl= models.CharField(max_length=500) #资质图片
    Remark = models.CharField(max_length=500,blank=True)  # 备注
    Status=models.IntegerField() # 代表有效，无效，待审核等状态

    class Meta:
        verbose_name_plural = '单位资质'

# 组织资质类别
class CredentialType(models.Model):
    IID = models.CharField(max_length=32)
    Name = models.CharField(max_length=200)
    Remark = models.CharField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = '资质类别'