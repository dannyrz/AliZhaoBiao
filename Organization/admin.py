import time
from django.contrib import admin
from Organization.models import Base
from Organization.models import Type
from Organization.models import Credential
from Organization.models import CredentialType

# Register your models here.

admin.site.register(Credential)
admin.site.register(CredentialType)


class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ['Name','IID', 'Remark']

admin.site.register(Type,OrganizationTypeAdmin)


class BaseAdmin(admin.ModelAdmin):
    list_display = [ 'Name','IID', 'CreditNumber','Contact','TelPhone','Status']
    radio_fields = {"Status": admin.HORIZONTAL}
    raw_id_fields = ("Type",)
    save_on_top=True;
    search_fields = ['Name','IID','CreditNumber']
    #description="这是单位基本资料"
    readonly_fields = ('IID',)

    def save_model(self, request, obj, form, change):
        if obj.IID is None or obj.IID=="":
            obj.IID = time.time()
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(BaseAdmin, self).get_form(request, obj, **kwargs)
        return form

    #def formfield_for_dbfield(self, db_field, **kwargs):
        #field = super(BaseAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        #if db_field.name == 'IID':
            #field.initial = time.time();
        #return field

admin.site.register(Base,BaseAdmin)