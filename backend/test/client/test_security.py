#!/usr/bin/env python3

"""
All things that visitors don't normally do
"""

import django.test
from django.test.utils import override_settings
from django.conf import settings
from rest_framework.test import APIClient
from submission.models import Submission, SubmissionResult
from problem.models import Problem, TestCase
from user.models import User
from file.models import File
from django.utils import timezone
import pytz

class SecurityAPITester(django.test.TestCase):
    """
    Something we don't usually do
    """

    def setUp(self):
        # Run once for every test method to setup clean data.
        # TODO: move something out of setUp

        admin_user = User.objects.create_superuser("admin", password="123456")
        #prob_file = File.objects.create(id=1, file=)

        # TODO: prob.problem_files.add
        # Hint: Don't use datetime.datetime.now()
        # ref: https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
        prob = Problem.objects.create(
            id=1, 
            name="A Test Problem", 
            deadline_time=timezone.now())

        # TODO: subm.submit_files.add
        subm = Submission.objects.create(
            id=1,
            problem=prob,
            user=admin_user
        )

        tesc = TestCase.objects.create(
            id=1,
            problem=prob,
            type='SIM'
        )

        subr = SubmissionResult.objects.create(
            id=1,
            submission=subm,
            testcase=tesc,
            status="DONE",
            grade=10,
            log="SOME_LOG",
            app_data="SOME_APPDATA"
        )

    def test_wrong_judger_secret(self):
        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET='SOMETHING_NEVER_MATCHES')
        resp = c.post('/oj/api/submit', {'problem': '1', 'submit_files': '[]'})
        # The TestCase in Django automatically disables csrf
        # ref: https://stackoverflow.com/questions/25003527/how-do-you-include-a-csrf-token-when-testing-a-post-endpoint-in-django
        self.assertNotContains(resp, 'CSRF', status_code=401) # 401 Unauthorized

    # make sure judger have no 127.0.0.1 given
    @override_settings(JUDGER_IP_WHITELIST=['127.0.0.10'])
    def test_judger_whitelist(self):
        self.assertTrue(settings.JUDGER_IP_WHITELIST[0] == '127.0.0.10')
        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET=settings.JUDGER_SECRET)
        resp = c.post('/oj/api/submit', {'problem': '1', 'submit_files': '[]'})
        # The TestCase in Django automatically disables csrf
        # ref: https://stackoverflow.com/questions/25003527/how-do-you-include-a-csrf-token-when-testing-a-post-endpoint-in-django
        self.assertNotContains(resp, 'CSRF', status_code=401) # 401 Unauthorized, since no Sess/Judger have given auth