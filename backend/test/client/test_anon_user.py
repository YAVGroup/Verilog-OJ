#!/usr/bin/env python3

"""
All things that an anonymous user could do shell be tested here
"""

import django.test
from rest_framework.test import APIClient
from submission.models import Submission, SubmissionResult
from problem.models import Problem, TestCase
from user.models import User
from file.models import File
from django.utils import timezone
import pytz

class AnonUserAPITester(django.test.TestCase):
    """An anonymous user should be able to do the following:

    - Submission:
        1. GET on all submission results
           - but without log and appdata
        2. NOT be able to submit new submissions
        3. NOT be able to do anything else on submission results
    
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
            grade=10,
            log="SOME_LOG",
            app_data="SOME_APPDATA",
            possible_failure="NA"
        )

    def test_submission_get(self):
        c = APIClient()
        resp = c.get('/api/submissions/')

        # This tests for both 200 and the content
        self.assertNotContains(resp, 'SOME_APPDATA', status_code=200)
        self.assertNotContains(resp, 'SOME_LOG', status_code=200)

    def test_submit(self):
        c = APIClient()
        resp = c.post('/api/submit', {'problem': '1', 'submit_files': '[]'})
        # The TestCase in Django automatically disables csrf
        # ref: https://stackoverflow.com/questions/25003527/how-do-you-include-a-csrf-token-when-testing-a-post-endpoint-in-django
        self.assertNotContains(resp, 'CSRF', status_code=401) # 401 Unauthorized
        
    def test_submission_result_get(self):
        c = APIClient()
        resp = c.get('/api/submission-results/')

        # This tests for both 200 and the content
        self.assertNotContains(resp, 'SOME_APPDATA', status_code=200)
        self.assertNotContains(resp, 'SOME_LOG', status_code=200)
        self.assertContains(resp, 'grade', status_code=200)
        self.assertContains(resp, 'NA', status_code=200)
    
    def test_submission_result_get_detail(self):
        c = APIClient()
        resp = c.get('/api/submission-results/1/')

        # This tests for both 200 and the content
        self.assertNotContains(resp, 'SOME_APPDATA', status_code=200)
        self.assertNotContains(resp, 'SOME_LOG', status_code=200)
        self.assertContains(resp, 'grade', status_code=200)
        self.assertContains(resp, 'NA', status_code=200)

    def test_submission_result_modify(self):
        c = APIClient()
        resp = c.post('/api/submission-results/',
            {"grade": 1, "log":"asdf", "app_data":"asdf", "submission": 1, "testcase": 1, "possible_failure": "NA"})

        self.assertEqual(resp.status_code, 401)

    def test_problem_get(self):
        c = APIClient()
        resp = c.get('/api/problems/')

        self.assertEqual(resp.status_code, 200)

    def test_problem_get_detail(self):
        c = APIClient()
        resp = c.get('/api/problems/1/')

        self.assertEqual(resp.status_code, 200)

    