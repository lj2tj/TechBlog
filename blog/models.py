#!/usr/bin/env python
#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from collections import defaultdict
from tinymce.models import HTMLField

class WebSiteAbout(models.Model):
    """
    Web site about information.
    """
    name = models.CharField('名称', max_length=20, null=True)
    value = models.CharField('显示值', max_length=100, null=True)
    comment = models.CharField('注释', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "网站介绍"
        verbose_name_plural = verbose_name


class Location(models.Model):
    """
    Geography location.
    """

    country = ('中国', '其它',)
    provence = ('北京', '天津', '上海', '重庆',)

class UserProfile(models.Model):
    """
    User profile class.
    """

    user = models.OneToOneField(User, unique=True, verbose_name=('用户'))
    photo = models.ImageField("头像", width_field=100, height_field=120, null=True)
    mobile_phone = models.CharField('移动电话', max_length=20, null=True)
    location = models.CharField('地址', max_length=200, null=True)

    class Meta:
        verbose_name = "站长"
        verbose_name_plural = verbose_name


class ArticleManage(models.Manager):
    """
    Article management class.
    """

    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items(), reverse=True)


class Article(models.Model):
    """
    DB model of article table.
    """

    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    objects = ArticleManage()

    title = models.CharField('标题', max_length=70)
    body = HTMLField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    views = models.PositiveIntegerField('浏览量', default=0, editable=False)
    download = models.PositiveIntegerField('下载次数', default=0, editable=False)
    topped = models.BooleanField('置顶', default=False)
    attachment = models.FileField(verbose_name='附件', upload_to='Articles', \
        storage=None, null=True, blank=True)
    category = models.ForeignKey('Category', verbose_name='分类', null=True, \
        on_delete=models.SET_NULL)
    tag = models.ForeignKey('Tag', verbose_name='标签集合', null=True, \
        blank=True)
    user = models.ForeignKey(User, editable=False, null=True, blank=True)

    def __str__(self):
        return self.title

    def toDict(self):  
        return dict([(attr, str(getattr(self, attr))) for attr in [f.name for f in self._meta.fields]])
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-last_modified_time']

    def get_absolute_url(self):
        """
        Get absolute url of article pages.
        """

        return reverse('blog:detail', kwargs={'article_id': self.pk})


class Category(models.Model):
    """
    DB model of article category.
    """

    DISPLAY_MODE = (
        ('l', 'List'),
        ('D', 'Detail'),
    )

    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    display = models.CharField('显示方式', max_length=1, default='l', choices=DISPLAY_MODE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    Article tag.
    """

    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class BlogComment(models.Model):
    """
    Article (blog) comment.
    """

    user_name = models.CharField('评论者名字', max_length=100)
    user_email = models.EmailField('评论者邮箱', max_length=255)
    body = HTMLField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]


class AppSettings(models.Model):
    """
    The basic settings of this web site.
    Include:
    WebSiteName
    UploadFilePath
    """
    name = models.CharField('名称', max_length=20, null=True)
    value = models.CharField('显示值', max_length=100, null=True)
    comment = models.CharField('注释', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "网站配置"
        verbose_name_plural = verbose_name

class WebSiteConfig:
    WebSiteName = ""
    ICP = ""