from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# 引入我们创建的表单类
from Project.form import CreateForm
from Project.models import Info
import time;

# Create your views here.

def create(request):
    if request.method == 'POST':  # 当提交表单时
        info = Info(IID=time.time())
        form = CreateForm(request.POST, instance=info)
        form.save()

        if form.is_valid():  # 如果提交的数据合法
            form.save()
            result=1;
            return HttpResponseRedirect("/project/create_result?result="+str(result))
    else:  # 当正常访问时
        form = CreateForm()
    return render(request, 'Project/create.html', {'form': form})

#下面的貌似用不上了
def create_result(request):
    result=request.GET['result']
    if result=="1":
        info = "提交成功！"
    else:
        info = "提交失败，请联系管理员！"
    return render(request, 'Project/create_result.html', {'info': info})