#!/usr/bin/env python3

"""
All things that an anonymous user could do shell be tested here
"""

import django.test, django.core.files
from rest_framework.test import APIClient
from submission.models import Submission, SubmissionResult
from problem.models import Problem, TestCase
from user.models import User
from file.models import File
from django.utils import timezone
import pytz, io, os

from django.conf import settings

class JudgerAPITester(django.test.TestCase):
    """An judger user should be able to do the following:

    - Submission:
        1. be able to submit new submission results
        2. be able to read new submissions
        3. be able to read problems
        4. be able to read testcases
        5. (TODO) be able to download file
        6. (TODO) no other permissions given
    
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
            app_data="SOME_APPDATA"
        )

        # Modify MEDIA_ROOT to change the place we store
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.old_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = os.path.join(BASE_PATH, "./tmp_storage/")

        fake_file_object = io.StringIO(initial_value='EXAMPLE_TEXT')
        file = File.objects.create(
            id=1,
            file=django.core.files.File(fake_file_object, name="example_file.txt"),
            name="example_file.txt"
        )

    def tearDown(self):
        settings.MEDIA_ROOT = self.old_root
        super().tearDown()


    def test_submit(self):
        """
        Judger should not have the permission to submit
        """
        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET=settings.JUDGER_SECRET)
        resp = c.post('/api/submit', {'problem': 1, 'submit_files': [1]})
        # The TestCase in Django automatically disables csrf
        # ref: https://stackoverflow.com/questions/25003527/how-do-you-include-a-csrf-token-when-testing-a-post-endpoint-in-django
        # print(resp.content.decode("utf-8"))
        self.assertEqual(resp.status_code, 403)

    def test_submission_result_uniqueness(self):
        """
        Because of the unique_together imposed by submission result
        """
        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET=settings.JUDGER_SECRET)
        resp = c.post('/api/submission-results/',
            {"grade": "1", "log":"asdf", "app_data":"asdf", "submission": "1", "testcase": "1"})
        #print(resp.content.decode("utf-8"))
        self.assertEqual(resp.status_code, 400)   # Bad request

    def test_submission_result_post(self):
        """
        Because of the unique_together imposed by submission result
        """
        # Delete the subm in advance
        SubmissionResult.objects.filter(id=1).delete()

        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET=settings.JUDGER_SECRET)
        resp = c.post('/api/submission-results/',
            {"grade": "1", "log":"asdf", "app_data":"asdf", "submission": "1", "testcase": "1"})
        #print(resp.content.decode("utf-8"))
        self.assertEqual(resp.status_code, 201)  # 201 Created

    def test_submission_result_get_detail(self):
        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET=settings.JUDGER_SECRET)
        resp = c.get('/api/submission-results/1/')

        # This tests for both 200 and the content
        self.assertContains(resp, 'SOME_APPDATA', status_code=200)
        self.assertContains(resp, 'SOME_LOG', status_code=200)
        self.assertContains(resp, 'grade', status_code=200)

    def test_problem_get_detail(self):
        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET=settings.JUDGER_SECRET)
        resp = c.get('/api/problems/1/')

        self.assertEqual(resp.status_code, 200)

    def test_testcase_get_detail(self):
        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET=settings.JUDGER_SECRET)
        resp = c.get('/api/problem-testcases/1/')

        self.assertEqual(resp.status_code, 200)

    def test_submission_get_detail(self):
        c = APIClient()
        c.credentials(HTTP_X_JUDGERSECRET=settings.JUDGER_SECRET)
        resp = c.get('/api/submissions/1/')

        # This tests for both 200 and the content
        self.assertEqual(resp.status_code, 200)

    