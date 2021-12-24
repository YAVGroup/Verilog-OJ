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
        "获得该用户提交的所有题目（仅id）"
        from problem.models import Problem
        from submission.models import Submission, SubmissionResult
        
        submission_id = Submission.objects.filter(user=self.id).values('problem').distinct().values('problem_id')

        submitted_problems = Problem.objects.filter(id__in=submission_id).values('id', 'logic_id', 'name').order_by('logic_id')

        return submitted_problems
    
    def get_ac_problems(self):
        "获得该用户AC的所有题目（仅id）"
        from problem.models import Problem
        from submission.models import Submission, SubmissionResult
        
        success_id = SubmissionResult.objects.filter(possible_failure="NONE", status="DONE").values('submission').values('submission_id')

        ac_problems_id = Submission.objects.filter(id__in=success_id, user=self.id).values('problem').distinct().values('problem_id')

        ac_problems = Problem.objects.filter(id__in=ac_problems_id).values('id', 'logic_id', 'name').order_by('logic_id')

        return ac_problems
    
    def get_undone_problems(self):
        from problem.models import Problem
        from submission.models import Submission, SubmissionResult

        success_id = SubmissionResult.objects.filter(possible_failure="NONE", status="DONE").values('submission').values('submission_id')

        ac_problems_id = Submission.objects.filter(id__in=success_id, user=self.id).values('problem').distinct().values('problem_id')

        undone_problems = Problem.objects.exclude(id__in=ac_problems_id).values('id', 'logic_id', 'name').order_by('logic_id')
        
        return undone_problems

    def get_ac_submission(self):
        "获得该用户AC的所有submission（仅id）"
        from submission.models import Submission, SubmissionResult
        ac_submission = set()
        ac_problems = set()
        for submission in self.get_submissions():
            if submission.is_ac() and submission.problem.id not in ac_problems:
                ac_submission.add(submission.id)
                ac_problems.add(submission.problem.logic_id)
        return ac_submission
    
    def get_total_score(self):
        "获得该用户提交的所有题目最大分数总和"
        # from submission.models import Submission, SubmissionResult
        
        # scores = {}
        # for submission in self.get_submissions():
        #     if submission.problem not in scores or submission.get_total_grade() > scores[submission.problem]:
        #         scores[submission.problem] = submission.get_total_grade()
        # return sum(scores.values())

        from problem.models import Problem
        from submission.models import Submission, SubmissionResult
        from django.db.models import Min, Sum
        
        # submission objects that are not succeed
        failed_id = SubmissionResult.objects.exclude(possible_failure="NONE", status="DONE").values('submission_id')

        # submission objects that shoule be successful, provided following intergrity requirements met 
        # NOTE: in multiple-testcase ones, testcase-submissionresult relations are implicitly assumed
        # So TODO: add integrity check for this
        success_id = Submission.objects.exclude(id__in=failed_id).values('id')

        # Submissions that are successful & has minimal id for one problem
        # 'SELECT MIN(`submission_submission`.`id`) AS `id__min` FROM `submission_submission` WHERE (`submission_submission`.`id` IN (SELECT V0.`id` FROM `submission_submission` V0 WHERE NOT (V0.`id` IN (SELECT U0.`submission_id` FROM `submission_submissionresult` U0 WHERE NOT (U0.`possible_failure` = NONE AND U0.`status` = DONE)))) AND `submission_submission`.`user_id` = 1) GROUP BY `submission_submission`.`problem_id` ORDER BY NULL'
        success_submission_id = Submission.objects.filter(id__in=success_id, user=self.id).values('problem').annotate(Min('id')).values("id__min")

        # all grades aggregated for all submissions above
        total_grades = SubmissionResult.objects.filter(submission_id__in=success_submission_id).aggregate(Sum('grade'))
        
        return total_grades['grade__sum']
