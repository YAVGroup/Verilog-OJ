from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True, help_text='用户ID')
    is_mail_authenticated = models.BooleanField(
        default=False,
        help_text='邮箱是否已经被验证（目前没用）'
    )
    student_id = models.CharField(
        max_length=10, null=True, blank=True,
        help_text='学生ID，标记是否经过统一身份验证'
    )
    
