from django.contrib import admin
from .models import Problem, TestCase
from django.urls import path
from django.template.response import TemplateResponse

class TestCaseInline(admin.StackedInline):
    model = TestCase
    extra = 0

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time', 'deadline_time', 'total_grade', 'related_testcases_id')
    inlines = [
        TestCaseInline,
    ]
    change_list_template = ['admin/custom_change_list.html']

    def total_grade(self, obj):
        return obj.get_total_grade()

    def related_testcases_id(self, obj):
        return ",".join([str(p.id) for p in obj.get_testcases()])
    
    def import_yaml_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            # Additional context
            foo=True
        )
        return TemplateResponse(request, "admin/import_yaml.html", context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_yaml/', self.admin_site.admin_view(self.import_yaml_view)),
        ]
        return my_urls + urls

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'related_problem', 'type', 'grade')

    def related_problem(self, obj):
        return obj.problem

admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase, TestCaseAdmin)