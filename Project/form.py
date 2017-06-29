# -*- coding: utf-8 -*-

from django.forms import ModelForm,Textarea,Select,TextInput
from Project.models import Info
from django.utils.translation import ugettext_lazy as _

# Create the form class.
class CreateForm(ModelForm):
    class Meta:
        model = Info
        fields = ['Name', 'FromName','BuildDimensions', 'Province', 'City', 'District','Contact','Telphone','Abstract']
        labels = {
            'Name': _('项目标题'),
        }
        help_texts = {
            'Name': _('输入你的项目名称. 如：xx公司弱电改造工程 , 智能监控别墅装修'),
        }
        error_messages = {
            'Name': {
                'max_length': _("This writer's name is too long."),
            },
        }
        widgets = {
            'FromName': TextInput(attrs={ 'class': 'form-control'}),
            'BuildDimensions': TextInput(attrs={ 'class': 'form-control'}),
            'Province': Select(attrs={ 'class': 'prov'}),
            'City': Select(attrs={'class':'city'}),
            'District': Select(attrs={ 'class': 'dist'}),
            'Contact': TextInput(attrs={'class': 'form-control'}),
            'Telphone': TextInput(attrs={'class': 'form-control'}),
            'Abstract': Textarea(attrs={'cols': 30, 'rows': 2, 'class': 'form-control'}),

        }

# Creating a form to add an project.
    #form = CreateForm()

# Creating a form to change an existing article.
    #article = Article.objects.get(pk=1)
    #form = ArticleForm(instance=article)