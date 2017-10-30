from django.shortcuts import render,redirect,HttpResponse
from rbac import models as rbac_models
from rbac.service.rbac import initial_permission

def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    elif request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        obj = rbac_models.User.objects.filter(username=username,password=password).first()
        if obj:
            initial_permission(request,obj)
            return redirect('/index/')


def index(request):
    return render(request,"index.html")

