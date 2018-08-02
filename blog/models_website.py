from django.db import models

# Create your models here.

class GlobalConfig(models.Model):

    website_title = models.CharField("网站名称", max_length=10)
    signature = models.CharField("网站签名", max_length=10)
    copyright = models.CharField("网站版权", max_length=10)
    address = models.CharField("地址", max_length=30)
    icp = models.CharField("ICP认证", max_length=20)


    def __str__(self):
        return r'网站全局配置'

    class Meta:
        db_table = 'config_global'
        managed = True
        verbose_name = '网站全局配置'
        verbose_name_plural = '网站全局配置'