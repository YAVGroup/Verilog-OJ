"""This module is supposed to be used in Django shell manually"""

from problem.models import Problem
from submission.models import Submission, SubmissionResult

def check_submissions():
    broken = []
    for submission in Submission.objects.all():
        sane, results, testcases = submission.check_integrity()
        if not sane:
            print(f"Bad submission: {submission.id}, Got {results} result(s) for {testcases} testcase(s)")
            print(f"- Submitted by {submission.user.username} (UID={submission.user.id})")
            broken.append(submission.id)
    
    return broken
