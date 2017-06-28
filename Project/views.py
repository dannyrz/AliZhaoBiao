from django.shortcuts import render
from django.http import HttpResponse
# 引入我们创建的表单类
from Project.form import CreateForm
import time;

# Create your views here.

def create(request):
    if request.method == 'POST':  # 当提交表单时
        form = CreateForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            form.save()
            return HttpResponse("Create Success.")

    else:  # 当正常访问时
        form = CreateForm(initial={'IID': time.time()})
    return render(request, 'Project/create.html', {'form': form})