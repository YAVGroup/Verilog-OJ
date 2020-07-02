from django.db import models
from user.models import User
from file.models import File

# TODO: 区分测试点编号

class Problem(models.Model):
    id = models.AutoField(primary_key=True, help_text='题目ID')
    name = models.CharField(max_length=20, help_text='题目名字')
#     creater = models.ForeignKey(
#         User,
#         null=True, on_delete=models.SET_NULL,
#         help_text='题目的创建者'
#     )
    create_time = models.TimeField(auto_now_add=True, help_text='题目的创建时间')
    deadline_time = models.TimeField(null=True, blank=True, help_text='题目的截止时间')
    problem_files = models.ManyToManyField(File, help_text='题目所用文件（描述等）')
    
    def get_testcases(self):
        return TestCase.objects.filter(problem=self)
    def get_total_grade(self):
        return sum([testcase.grade for testcase in self.get_testcases()])

class TestCase(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        help_text='测试点所属的题目'
    )
    TYPE_CHOICES = [('SIM', 'Simulation'),]
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES,
        help_text='测试点类型'
    )
    testcase_files = models.ManyToManyField(File, help_text='测试点所用文件')
    grade = models.IntegerField(default=10, help_text='测试点分值')
