from django.contrib import admin
from .models import Problem, TestCase
from file.models import File
from django.urls import path
from django.template.response import TemplateResponse
import sys, io
from django.db import transaction
import django.core.files

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


    def import_yaml(self, yaml_data):
        log = ""
        success = False

        log += "Importing pyyaml library...\n"
        try:
            import yaml
        except ImportError:
            log += "Error: Failed to import pyyaml library, make sure the server side have pyyaml installed.\n"
            return log, success

        ys = yaml.load(yaml_data, Loader=yaml.SafeLoader)
        try:
            num_problems = len(ys['problems'])
        except:
            log += "Error while retriving ys['problems'] and its length: {}\n".format(sys.exc_info()[1])
            log += "Make sure your Yaml is correct!\n"
            return log, success

        #log += "Yaml parsed: {}\n".format(ys)
        log += "Got {} problems..\n".format(num_problems)
        validated_probs = []
        for i in range(0, num_problems):
            problem_info = {}
            try:
                def read_optional(name):
                    return ys_prob[name] if name in ys_prob else None
                
                def read_optionals(name, op):
                    ret = read_optional(name)
                    if ret is None:
                        return None
                    return [op(i) for i in ret]

                def read_file_info(info):
                    if info is None:
                        return None
                    file_info = {}
                    file_info['name'] = info['name']
                    file_info['content'] = info['content']
                    return file_info

                def read_testcase(info):
                    testcase_info = {}
                    testcase_info['type'] = info['type']
                    testcase_info['grade'] = info['grade']
                    testcase_info['testcase_files'] = []
                    for f in testcase_info['testcase_files']:
                        info = read_file_info(f)
                        testcase_info['testcase_files'].append(f)
                    return testcase_info

                ys_prob = ys['problems'][i]
                problem_info['name'] = ys_prob['name']
                problem_info['description'] = ys_prob['description']
                problem_info['description_input'] = ys_prob['description_input']
                problem_info['description_output'] = ys_prob['description_output']
                problem_info['app_data'] = read_optional('app_data')

                problem_info['template_code_file'] = read_file_info(read_optional('template_code_file'))
                problem_info['description_files'] = read_optionals('description_files', read_file_info)
                problem_info['judge_files'] = read_optionals('judge_files', read_file_info)
                problem_info['testcases'] = read_optionals('testcases', read_testcase)
                
                log += str(problem_info)
                log += "\n"
            except:
                log += "Error while retriving Problem #{}: {}\n".format(i, sys.exc_info()[1])
                log += "Make sure your Yaml is correct!\n"
                return log, success

            validated_probs.append(problem_info)

        # Save in db
        def save_file_to_db(file_info):
            file_inst = File.objects.create(
                name=file_info['name'],
                file=django.core.files.File(io.StringIO(initial_value=file_info['content']), name=file_info['name'])
            )
            return file_inst

        def save_testcase_to_db(prob_inst, tinfo):
            f_insts = []
            for finfo in tinfo['testcase_files']:
                 f_insts.append(save_file_to_db(finfo))

            t_inst = TestCase.objects.create(
                problem=prob_inst,
                grade=tinfo['grade'],
                type=tinfo['type'],
            )
            for f_inst in f_insts:
                t_inst.testcase_files.add(f_inst)
            
            t_inst.save()

        with transaction.atomic():
            log += "Saving to the database...\n"
            for prob in validated_probs:
                log += "Saving problem named {}...\n".format(prob['name'])
                prob_inst = Problem.objects.create(
                    name=prob['name'],
                    description=prob['description'],
                    description_input=prob['description_input'],
                    description_output=prob['description_output'],
                    app_data="" if prob['app_data'] is None else prob['app_data']
                )

                if prob['template_code_file'] is not None:
                    file_inst = save_file_to_db(prob['template_code_file'])
                    prob_inst.template_code_file = file_inst
                
                if prob['description_files'] is not None:
                    for finfo in prob['description_files']:
                        file_inst = save_file_to_db(finfo)
                        prob_inst.description_files.add(file_inst)
                
                if prob['judge_files'] is not None:
                    for finfo in prob['judge_files']:
                        file_inst = save_file_to_db(finfo)
                        prob_inst.judge_files.add(file_inst)
                
                if prob['testcases'] is not None:
                    log += "Saving related testcases..\n"
                    # Save related testcase first
                    for tinfo in prob['testcases']:
                        test_inst = save_testcase_to_db(prob_inst, tinfo)

                prob_inst.save()

        success = True
        return log, success
        

    def import_yaml_view(self, request):

        # TODO: avoid duplicate import
        stat_msg = ""
        if request.method == 'POST':
            if 'yaml_context' not in request.POST:
                stat_msg += "Error: yaml_context should be available in POST request"
            else:
                stat_msg += "Processing begin\n"
                log, success = self.import_yaml(request.POST['yaml_context'])
                stat_msg += log
                if not success:
                    stat_msg += "Operation failed.\n"
                else:
                    stat_msg += "Operation completed successfully.\n"
        
        context = dict(
            self.admin_site.each_context(request),
            title="从 Yaml 导入 problem",
            # Additional context
            status_message=stat_msg if stat_msg != "" else "No messages available."
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