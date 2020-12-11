from django.contrib import admin
from .models import User
from django.http import HttpResponse
import io, csv
from submission.models import Submission, SubmissionResult


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','student_id', 'problem_count', 'ac_count','total_score')
    actions = ['export_csv']
    
    def problem_count(self,obj):
        return len(obj.get_submitted_problems())

    def ac_count(self,obj):
        return len(obj.get_ac_problems())

    def total_score(self, obj):
        return obj.get_total_score()


    def export_csv(self,request,queryset):
        usr_all = []

        for user_info in queryset:
            usr = {}
            usr['student_id'] = user_info.student_id
            usr['username'] = user_info.username

            user_ac = user_info.get_ac_submission()
            if len(user_ac) > 0:
                for p_inst in user_ac:
                    submit = Submission.objects.filter(id = p_inst)
                    usr[submit[0].problem.name] = submit[0].get_total_grade()
            usr_all.append(usr)
                
        writer = io.StringIO()
        csv_writer = csv.writer(writer)
        for row in usr_all:
            csv_writer.writerow(
                [
                    row['student_id'] if row['student_id'] != None else "N/A",
                    row['username']
                ]
            )
        
        response = HttpResponse(content_type="text/plain")
        response.write(writer.getvalue())
        return response

    export_csv.short_description = "Export users to csv"

admin.site.register(User,UserAdmin)