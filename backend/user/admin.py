from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.http import HttpResponse
import io, csv
from submission.models import Submission, SubmissionResult
from problem.models import Problem
from django.utils import timezone

class UserAdmin(BaseUserAdmin):
    list_display = ('username','student_id', 'problems_done', 'ac_problems_count','total_score')
    actions = ['export_csv']
    
    def problems_done(self,obj):
        return len(obj.get_submitted_problems())

    def ac_problems_count(self,obj):
        return len(obj.get_ac_problems())

    def total_score(self, obj):
        return obj.get_total_score()


    def export_csv(self, request, queryset):
        writer = io.StringIO()
        csv_writer = csv.writer(writer)
        total_problems = Problem.objects.all().count()
        time_now = str(timezone.now())

        # csv_writer.writerow(
        #     [
        #         f"Exported at {time_now} with {total_problems} problem(s) in database",
        #         "",
        #         "",
        #         "",
        #         "",
        #         ""
        #     ]
        # )

        csv_writer.writerow(
            [
                "Username",
                "USTC-CAS ID",
                "# of problems submitted",
                "# of problems undone",
                "# of problems accepted",
                "Total score"
            ]
        )

        for user in queryset:
            user_ac = user.get_ac_problems()
            user_undone = user.get_undone_problems()
            user_submitted = user.get_submitted_problems()
            
            csv_writer.writerow(
                [
                    user.username,
                    user.student_id,
                    user_submitted.count(),
                    user_undone.count(),
                    user_ac.count(),
                    user.get_total_score()
                ]
            )
        
        response = HttpResponse(
            content_type="text/csv",
            headers={'Content-Disposition': f'attachment; filename="{time_now}_{total_problems}probs.csv"'}    
        )
        response.write(writer.getvalue())
        return response

    export_csv.short_description = "Export users to csv"

admin.site.register(User,UserAdmin)