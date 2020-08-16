from django.contrib import admin
from .models import Submission, SubmissionResult

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'user', 'submit_time', 'is_ac', 'grade_got', 'problem_score_total')
    list_filter = ('problem__name', 'user', 'submit_time')
    
    def have_judged(self, obj):
        return obj.have_judged()
    # make a pretty boolean icon
    # ref: https://stackoverflow.com/questions/8227023/list-display-boolean-icons-for-methods
    have_judged.boolean = True

    def is_ac(self, obj):
        return obj.is_ac()
    is_ac.boolean = True

    def grade_got(self, obj):
        return obj.get_total_grade()

    def problem_score_total(self, obj):
        return obj.problem.get_total_grade()

class SubmissionResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'submit_time', 'submission', 'testcase', 'grade')
    list_filter = ('status', 'grade', 'submit_time', 'testcase')

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(SubmissionResult, SubmissionResultAdmin)