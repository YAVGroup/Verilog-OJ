from datetime import datetime
from django.db import models
from user.models import User
from problem.models import Problem

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='发帖人'
    )

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        help_text='讨论相关题目'
    )

    title = models.CharField(max_length=50,help_text='讨论标题')
    description = models.TextField(help_text='讨论内容描述（文字）')

    def get_comments(self):
        "获取所有该 topic 的评论（返回时间，用于排序）"
        comment_ids = Comment.objects.filter(topic=self).values('update_time')

        return comment_ids

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name=u'修改时间')

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    replyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,       
        help_text='回帖人'
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        help_text='帖子'
    )

    text = models.TextField(help_text='评论')
    is_removed = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text='父评论')
    likes_count = models.PositiveIntegerField(default=0,verbose_name=u'点赞数')

    create_time = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=u'修改时间', auto_now_add=True)

    def __str__(self):
        return self.topic.title


