from django.db import models

from tinymce.models import HTMLField

# Create your models here.

class Category(models.Model):
    """
    DB model of article category.
    """

    name = models.CharField('类别', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    description = models.CharField('说明', max_length=200, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_category'
        managed = True
        verbose_name = '类别'
        verbose_name_plural = '类别'
        ordering = ['id']

class Article(models.Model):
    """
    DB model of article table.
    """

    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发布'),
    )

    title = models.CharField('标题', max_length=50, null=False)
    body = HTMLField('正文', max_length=10000, null=False)
    category = models.ForeignKey('Category', verbose_name='分类', null=False, \
        on_delete=models.PROTECT)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    views = models.PositiveIntegerField('浏览量', default=0, editable=False)
    likes = models.PositiveIntegerField('点赞数', default=0, editable=False)
    
    news_img = models.ImageField('文章展示图片', null=True, blank=True, upload_to="Article/Img/")
    attachment_id = models.FileField('附件', null=True, blank=True, upload_to="Article/File/")
    download_times = models.PositiveIntegerField('下载次数', default=0, editable=False)
    is_top = models.BooleanField("是否优先展示", default=False)
    top_level = models.PositiveIntegerField("优先级级别", default=0)
    keywords = models.CharField("文章关键字", max_length=50, null=True)
    description = models.CharField("文章描述", max_length=150, null=True)


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blog_article'
        managed = True
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_time']

class Comment(models.Model):
    """
    Article (blog) comment.
    """

    user_name = models.CharField('评论者名字', max_length=20, null=False)
    user_email = models.EmailField('评论者邮箱', max_length=100, null=False)
    body = HTMLField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]

    class Meta:
        db_table = 'blog_comment'
        managed = True
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'


