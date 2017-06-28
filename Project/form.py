# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from Project.models import Info

# Create the form class.
class CreateForm(ModelForm):
    class Meta:
        model = Info
        fields = ['Name', 'FromName','BuildDimensions', 'Province', 'City', 'District','Abstract']

# Creating a form to add an project.
    #form = CreateForm()

# Creating a form to change an existing article.
    #article = Article.objects.get(pk=1)
    #form = ArticleForm(instance=article)