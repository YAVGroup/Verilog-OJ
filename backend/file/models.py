from django.db import models

class File(models.Model):
    uuid = models.IntegerField(primary_key=True, help_text='文件的UUID')
    file = models.FileField(upload_to='')
    name = models.CharField(max_length=100, help_text='文件名')
    size = models.IntegerField(help_text='文件大小')
    update_time = models.TimeField(auto_now=True, help_text='修改时间')