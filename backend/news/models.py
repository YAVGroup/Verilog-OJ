from django.db import models
from file.models import File

# Create your models here.
class News(models.Model):
    id = models.AutoField(primary_key=True, help_text='News ID')
    title = models.CharField(max_length=40, help_text='News title')
    create_time = models.DateTimeField(auto_now_add=True, help_text='News creation time')
    content = models.TextField(help_text='News content')
    related_files = models.ManyToManyField(File, help_text='File attached with the news', blank=True)

    def __str__(self):
        return self.title