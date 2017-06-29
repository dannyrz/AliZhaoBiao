from django.contrib import admin
from Project.models import Info

# Register your models here.
class InfoAdmin(admin.ModelAdmin):
    list_display = [ 'Name', 'SerialNumber','FromName','City','District','BuildDimensions','Contact','Telphone','Status']
    radio_fields = {"Status": admin.HORIZONTAL}
    save_on_top=True;
    search_fields = ['Name','IID','SerialNumber']
    #description="这是单位基本资料"
    readonly_fields = ('IID',)

    def save_model(self, request, obj, form, change):
        if obj.IID is None or obj.IID=="":
            obj.IID = time.time()
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(InfoAdmin, self).get_form(request, obj, **kwargs)
        return form


admin.site.register(Info,InfoAdmin)
