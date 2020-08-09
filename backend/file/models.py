from django.db import models
import os, time

class File(models.Model):
    id = models.AutoField(primary_key=True, help_text='文件的UUID')
    file = models.FileField(upload_to='')
    name = models.CharField(max_length=100, blank=True, null=True, editable=False, help_text='文件名')
    
    def save(self, **kwargs):
        # 先保存数据，然后重新修改，这是因为我们必须先操作数据库才能得到生成的ID
        super(File, self).save(**kwargs)
        
        # 修改文件名，加上ID和日期
        old_name = self.file.name
        self.name = old_name
        new_name = '%s_%s_%s' % (self.pk, time.strftime("%Y%m%d", time.localtime(time.time())), old_name)
        
        # 重新保存文件
        storage = self.file.storage
        storage.delete(new_name)
        storage.save(new_name, self.file)
        storage.delete(old_name)
        self.file.name = new_name
        
        # 重新更新数据库
        kwargs['force_insert'] = False
        kwargs['force_update'] = True
        super(File, self).save(**kwargs)