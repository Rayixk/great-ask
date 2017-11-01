from django.shortcuts import render, redirect, HttpResponse
from rbac import models as rbac_models
from rbac.service.rbac import initial_permission
from . import models


class SurveyObj(object):
    def __init__(self, survey_obj):
        self.survey_obj = survey_obj
        self.single_choices = None
        self.multi_choices = None
        self.text_inputs = None
        self.textarea_inputs = None
        self.init()

    def init(self):
        self.single_choices = [obj for obj in self.survey_obj.choice_boxes.all() if obj.type == 1]
        self.multi_choices = [obj for obj in self.survey_obj.choice_boxes.all() if obj.type == 2]
        self.text_inputs = [obj for obj in self.survey_obj.input_boxes.all() if obj.type == 1]
        self.textarea_inputs = [obj for obj in self.survey_obj.input_boxes.all() if obj.type == 2]


def login(request):
    if request.method == "POST":
        # if :

        username = request.POST.get("username")
        password = request.POST.get("password")
        obj = rbac_models.User.objects.filter(username=username, password=password).first()
        if obj:
            survey_id = request.GET.get("survey_id")
            if survey_id and hasattr(obj.userinfo, "student"):
                request.session["student_id"] = obj.userinfo.student.pk
                return redirect("/survey/{}".format(survey_id, ))
            else:
                initial_permission(request, obj)
                return redirect('/index/')
    return render(request, "login.html")


def index(request):
    return render(request, "index.html")


def show_survey(request, survey_id):

    if request.method=="POST":
        print(request.POST)
        return HttpResponse("xxxx")

    # 未登录请先登录
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect('/login/?survey_id=%s' % survey_id)

    # 问卷不存在检查url
    survey_obj = models.Survey.objects.filter(pk=survey_id).first()
    if not survey_obj:
        return HttpResponse("问卷不存在,请检查url是否正确")

    # 不是本班学生不要填写问卷
    student_obj = models.Student.objects.filter(pk=student_id).first()
    is_our_class = False
    for clazz in survey_obj.class_list.all():
        if student_obj in clazz.student_set.all():
            is_our_class = True
            break
    if not is_our_class:
        return HttpResponse("非本班学生,请勿填写本问卷")

    survey_plus = SurveyObj(survey_obj)

    context = {
        "survey_plus": survey_plus,
    }

    return render(request, "show_survey.html", context)
