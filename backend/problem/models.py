from django.db import models
from user.models import User
from file.models import File

class Problem(models.Model):
    id = models.AutoField(primary_key=True, help_text='题目ID')
    name = models.CharField(max_length=20, help_text='题目名字')
    create_time = models.DateTimeField(auto_now_add=True, help_text='题目的创建时间')
    deadline_time = models.DateTimeField(null=True, blank=True, help_text='题目的截止时间')
    
    description = models.TextField(help_text='题目描述（文字）')
    description_input = models.TextField(help_text='输入描述（文字）')
    description_output = models.TextField(help_text='输出描述（文字）')
    description_files = models.ManyToManyField(File, help_text='描述文件', related_name='description', blank=True)
    
    app_data = models.TextField(help_text='样例用到的波形图', blank=True)
    judge_files = models.ManyToManyField(File, help_text='评测所用文件', related_name='judge', blank=True)
    
    def get_testcases(self):
        "获得该题目所有测试点"
        return TestCase.objects.filter(problem=self)
    
    def get_total_grade(self):
        "获得该题目测试点分值之和"
        return sum([testcase.grade for testcase in self.get_testcases()])
    
    def get_submitted_users(self):
        "获得提交了该题目的用户（仅id）"
        from submission.models import Submission
        submissions = Submission.objects.filter(problem=self)
        users = set()
        for submission in submissions:
            users.add(submission.user.id)
        return list(users)
    
    def get_ac_users(self):
        "获得AC了该题目的用户（仅id）"
        from submission.models import Submission
        submissions = Submission.objects.filter(problem=self)
        users = set()
        for submission in submissions:
            if submission.is_ac():
                users.add(submission.user.id)
        return list(users)
    
    def __str__(self):
        return self.name

class TestCase(models.Model):
    id = models.AutoField(primary_key=True, help_text='Testcase ID')
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
    testcase_files = models.ManyToManyField(File, help_text='测试点所用文件', blank=True)
    grade = models.IntegerField(default=10, help_text='测试点分值')

    def __str__(self):
        return "TestCase #{} (Problem #{}, {})".format(
            self.id, self.problem.id, self.problem.name
            )