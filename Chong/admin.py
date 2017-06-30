from django.contrib import admin
from Chong.models import Task
import time;

class TaskAdmin(admin.ModelAdmin):
    list_display = [ 'Name', 'IID','Charset','WorkInterval','ThreadNumber','Status']
    radio_fields = {"Status": admin.HORIZONTAL}
    save_on_top=True;
    search_fields = ['Name','IID']
    #description="这是单位基本资料"
    readonly_fields = ('IID',)

    def save_model(self, request, obj, form, change):
        if obj.IID is None or obj.IID=="":
            obj.IID = time.time()
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskAdmin, self).get_form(request, obj, **kwargs)
        return form


admin.site.register(Task,TaskAdmin)