from django.db import models
from django.contrib.auth.models import User

from tinymce.models import HTMLField

class UserProfile(models.Model):
    """
    User profile class.
    """

    user = models.OneToOneField(User, unique=True, verbose_name=('作者'), on_delete=models.CASCADE)
    #photo = models.ImageField("头像", width_field=100, height_field=120, null=True)
    about = HTMLField('站长介绍')
    qq = models.CharField('qq', max_length=20, null=True, blank=True)
    toutiao = models.CharField('头条号', max_length=20, null=True, blank=True)
    github = models.CharField('github', max_length=20, null=True, blank=True)
    location = models.CharField('地址', max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'account_owner'
        verbose_name = "作者"
        verbose_name_plural = verbose_name
        