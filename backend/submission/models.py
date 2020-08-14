from django.db import models

from problem.models import Problem, TestCase
from file.models import File
from user.models import User

class Submission(models.Model):
    id = models.AutoField(primary_key=True, help_text='提交ID')
    problem = models.ForeignKey(
        Problem,
        on_delete=models.SET_NULL, null=True,
        help_text='提交的题目',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='提交的用户'
    )
    submit_time = models.DateTimeField(auto_now_add=True, help_text='提交时间')
    submit_files = models.ManyToManyField(File, help_text='提交的文件（代码等）')
    
    def get_results(self):
        "获得该次提交对应的所有测试点结果"
        return SubmissionResult.objects.filter(submission=self)
    
    def get_total_grade(self):
        "获得该次提交的总分数"
        return sum([result.grade for result in self.get_results()])
    
    def have_judged(self):
        "判断是否已经评测完毕"
        if self.problem is None:
            return False
        else:
            return len(self.get_results()) == len(self.problem.get_testcases())
    
    def is_ac(self):
        "判断该次提交是否AC"
        for result in self.get_results():
            if not result.is_ac():
                return False
        return True

class SubmissionResult(models.Model):
    id = models.AutoField(primary_key=True, help_text='提交结果ID')

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('JUDGING', 'Judging'),
        ('DONE', 'Done'),
        ('ERROR', 'Error')
    ]

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        help_text='The current status of this submission result'
    )

    POSSIBLE_FAILURE_CHOICES = [
        ('CE', 'Compile Error'),
        ('RES_LIM_EXCEED', 'Resource Limitation Exceeded'),
        ('NONE', 'No error'),
        ('TIME_LIM_EXCEED', 'Time Limitation Exceeded'),
        # When it's in PENDING or JUDGING we use this
        ('NA', 'Not available')
    ]

    possible_failure = models.CharField(
        max_length=20, choices=POSSIBLE_FAILURE_CHOICES,
        help_text='Possible failure of this submission result'
    )

    submit_time = models.DateTimeField(auto_now_add=True, help_text='结果提交时间')
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        help_text='某个测试点结果所属的提交'
    )
    testcase = models.ForeignKey(
        TestCase,
        on_delete=models.CASCADE,
        help_text='某个测试点结果所属的测试点'
    )
    grade = models.IntegerField(help_text='本测试点所得的分数')
    log = models.TextField(help_text='The log generated along the process')
    app_data = models.TextField(help_text='Data associated with this result (waveform, etc)')
    
    class Meta:
        unique_together = (('submission', 'testcase'),)
    
    def is_ac(self):
        "判断该测试点是否AC"
        return self.grade == self.testcase.grade