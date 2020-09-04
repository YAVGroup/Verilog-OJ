from django.contrib import admin
import django.contrib.messages
from .models import File
from django.contrib.admin import widgets
import django.urls

class DownloadFileWidget(widgets.AdminFileWidget):
    id = None
    template_name = 'admin/widgets/custom_file_input.html'

    def __init__(self, id, attrs=None):
        self.id = id
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        print(self, context, name, value, attrs, self.id)
        # ref on the name of the file retrieval API: https://www.django-rest-framework.org/api-guide/routers/
        # Django uses widgets.value for the FieldFile (uncomment the print and you can find it)
        # My template have modified widget.value.url to widget.url to bypass this
        context['widget'].update({
            'url': django.urls.reverse('file-detail', kwargs={'pk': self.id}) 
        })
        return context

# ref: https://stackoverflow.com/questions/51492206/how-can-i-add-a-link-to-download-a-file-in-a-django-admin-detail-page/
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_ref' ,'ref_in_problem', 'ref_in_testcase', 'ref_in_submission')
    my_id_for_formfield = None
    actions = ['clear_unreferenced']

    def clear_unreferenced(self, request, queryset):
        item_cleaned = 0
        for f_inst in queryset:
            if self.total_ref(f_inst) == 0:
                f_inst.delete()
                item_cleaned += 1
        self.message_user(request, 
            "{} unreferenced file(s) deleted.".format(item_cleaned),
            django.contrib.messages.SUCCESS)
    clear_unreferenced.short_description = "Delete unreferenced files"
    

    def total_ref(self, obj):
        return self.ref_in_problem(obj) + self.ref_in_submission(obj) + self.ref_in_testcase(obj)

    def ref_in_problem(self, obj):
        return len(obj.problem_set.all())

    def ref_in_testcase(self, obj):
        return len(obj.testcase_set.all())

    def ref_in_submission(self, obj):
        return len(obj.submission_set.all())

    # Notice: This rely on the calling sequence (get_form -> formfield_for_dbfield)
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.my_id_for_formfield = obj.id
        return super().get_form(request, obj=obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if self.my_id_for_formfield:
            if db_field.name == 'file':
                kwargs['widget'] = DownloadFileWidget(id=self.my_id_for_formfield)

        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(File, FileAdmin)