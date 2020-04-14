from django.contrib import admin
from .models import Submission, SubmissionResult

admin.site.register(Submission)
admin.site.register(SubmissionResult)