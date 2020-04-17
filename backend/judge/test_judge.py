
from django.test import TestCase
from django.utils import timezone

from judge.models import *
import re
import random
import string
import subprocess
import os
import sys
import time
import filecmp


class QuestionModelTests(TestCase):

    def test_case_0(self):
        print("\nTest 0:")
        print("Hello world")
        subprocess.run("pwd")

    def test_case_1_generate(self):
        print("\nTest 1:")
        name = generate_submit_zone()
        print(name)
        print("Input to continue:")
        wait_var = input()
        subprocess.run(
            "rm" + " -rf {foldername}".format(foldername=name), shell=True)

    def test_case_2_iverilog_test(self):
        print("\nTest 2:")
        perform_judge_iverilog_version(None)
