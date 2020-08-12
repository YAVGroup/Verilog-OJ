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
    
    def get_submissions(self):
        "获得该用户的所有提交记录"
        from submission.models import Submission, SubmissionResult
        
        return Submission.objects.filter(user=self)
    
    def get_submitted_problems(self):
        "获得该用户提交的所有题目"
        from submission.models import Submission, SubmissionResult
        
        submitted_problems = set()
        for submission in self.get_submissions():
            submitted_problems.add(submission.problem)
        return list(submitted_problems)
    
    def get_ac_problems(self):
        "获得该用户AC的所有题目"
        from submission.models import Submission, SubmissionResult
        
        ac_problems = set()
        for submission in self.get_submissions():
            if submission.is_ac():
                ac_problems.add(submission.problem)
        return list(ac_problems)
    
    def get_total_score(self):
        "获得该用户提交的所有题目最大分数总和"
        from submission.models import Submission, SubmissionResult
        
        scores = {}
        for submission in self.get_submissions():
            if submission.problem not in scores or submission.get_total_grade() > scores[submission.problem]:
                scores[submission.problem] = submission.get_total_grade()
        return sum(scores.values())