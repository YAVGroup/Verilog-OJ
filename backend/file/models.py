from django.db import models

class File(models.Model):
    id = models.AutoField(primary_key=True, help_text='文件的UUID')
    file = models.FileField(upload_to='')
    name = models.CharField(max_length=100, blank=True, null=True, editable=False, help_text='文件名')
    
    def save(self, **kwargs):
        # 先保存数据，然后重新修改，这是因为我们必须先操作数据库才能得到生成的ID       
        # 修改文件名，加上ID和日期
        self.name = self.file.name    
  
        super(File, self).save(**kwargs)

    def __str__(self):
        return self.name

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    instance.file.storage.delete(instance.file.name)