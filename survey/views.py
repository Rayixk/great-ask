import json

from django.shortcuts import render, redirect, HttpResponse
from rbac import models as rbac_models
from rbac.service.rbac import initial_permission
from django.db import transaction
from . import models

SINGLE_CHOICES = "single_choices"
MULTI_CHOICES = "multi_choices"
SCORE_CHOICES = "score_choices"
TEXT_INPUTS = "text_inputs"
TEXTAREA_INPUTS = "textarea_inputs"


# class SurveyObj(object):
#     def __init__(self, survey_obj):
#         self.survey_obj = survey_obj
#         self.init()
#
#     def init(self):
#         setattr(self, SINGLE_CHOICES, [obj for obj in self.survey_obj.items if obj.type == 1])
#         setattr(self, MULTI_CHOICES, [obj for obj in self.survey_obj.items if obj.type == 2])
#         setattr(self, SCORE_CHOICES, [obj for obj in self.survey_obj.items if obj.type == 3])
#         setattr(self, TEXT_INPUTS, [obj for obj in self.survey_obj.items if obj.type == 4])
#         setattr(self, TEXTAREA_INPUTS, [obj for obj in self.survey_obj.items if obj.type == 5])


def login(request):
    if request.method == "POST":
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


def save_one(student, question_id, answer):
    """
    保存一个选择题或者填空题
    :param student: 学生对象
    :param question: 一个题的类型和id,如multi_choice2:指代的是多选题第二题
    :param answer: 该题提交答案
    :param survey_id: 调查问卷id
    """

    # # 单选题
    # if SINGLE_CHOICES[:-1] in question:
    #     _, question_id = question.split(SINGLE_CHOICES[:-1])
    #     models.ChoiceRecord.objects.create(user=student, survey_id=survey_id, question_id=question_id,
    #                                        answer_id=answer[0])
    # # 多选题
    # elif MULTI_CHOICES[:-1] in question:
    #     _, question_id = question.split(MULTI_CHOICES[:-1])
    #     for answer_id in answer:
    #         models.ChoiceRecord.objects.create(user=student, survey_id=survey_id, question_id=question_id,
    #                                            answer_id=answer_id)
    # # 填空题 - text
    # elif TEXT_INPUTS[:-1] in question:
    #     _, question_id = question.split(TEXT_INPUTS[:-1])
    #     models.InputRecord.objects.create(user=student, survey_id=survey_id, question_id=question_id, answer=answer[0])
    #
    # # 填空题-area
    # elif TEXTAREA_INPUTS[:-1] in question:
    #     _, question_id = question.split(TEXTAREA_INPUTS[:-1])
    #     models.InputRecord.objects.create(user=student, survey_id=survey_id, question_id=question_id, answer=answer[0])



def save_data(request):
    response = "提交成功"

    student = models.Student.objects.filter(pk=request.session.get("student_id")).first()
    print(request.POST)

    choice_records = []
    input_records = []

    for question_id in request.POST:
        if question_id =="csrfmiddlewaretoken":
            continue
        answer = request.POST.getlist(question_id)
        question_type = models.SurveyItem.objects.filter(pk=question_id).first().type

        if question_type == 3 or question_type == 2:  # 多选题
            for choice_id in answer:
                obj = models.ChoiceRecord(user=student, question_id=question_id, answer_id=choice_id)
                choice_records.append(obj)
        elif question_type == 1:  # 单选题
            obj = models.ChoiceRecord(user=student, question_id=question_id, answer_id=answer[0])
            choice_records.append(obj)
        elif question_type == 4 or question_type == 5:  # 填空题
            obj = models.InputRecord(user=student, question_id=question_id, answer=answer[0])
            input_records.append(obj)

    #保存
    models.ChoiceRecord.objects.bulk_create(choice_records)
    models.InputRecord.objects.bulk_create(input_records)


    # try:
    #     with transaction.atomic():
    #         for k in request.POST:
    #             save_one(student, k, request.POST.getlist(k))
    # except Exception as e:
    #     response = str(e)
    return response


def show_survey(request, survey_id):
    if request.method == "POST":
        response = save_data(request)
        return HttpResponse(response)

    # 未登录请先登录
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect('/login/?survey_id=%s' % survey_id)

    # 问卷不存在检查url
    survey_obj = models.Survey.objects.filter(pk=survey_id).first()
    if not survey_obj:
        return HttpResponse("问卷不存在,请检查url是否正确")

    # # 不是本班学生不要填写问卷
    # student_obj = models.Student.objects.filter(pk=student_id).first()
    # is_our_class = False
    # for clazz in survey_obj.class_list.all():
    #     if student_obj in clazz.student_set.all():
    #         is_our_class = True
    #         break
    # if not is_our_class:
    #     return HttpResponse("非本班学生,请勿填写本问卷")

    # survey_plus = SurveyObj(survey_obj)

    context = {
        "survey_obj": survey_obj,
    }

    return render(request, "show_survey.html", context)


def save_survey_data(request):
    """将新建的survey信息保存到数据库"""
    response = {"status": True}
    res = json.loads(request.POST.get("questions"), encoding="utf-8")
    survey_title = res[0]
    questions = res[1:]
    print(res)
    items = []

    try:
        with transaction.atomic():
            for question in questions:
                if question["type"] == "4" or question["type"] == "5" :#填空题
                    item = models.SurveyItem.objects.filter(title=question["name"], type=question["type"]).first()
                    if not item:
                        item = models.SurveyItem.objects.create(title=question["name"], type=question["type"])

                else: #选择题
                    item = models.SurveyItem.objects.create(title=question["name"], type=question["type"])
                    item_choices=[]
                    if question["choices"]:#说明是选择题
                        for title in question["choices"]:
                            choice_obj = models.Choice.objects.filter(title=title).first()
                            if not choice_obj:
                                choice_obj = models.Choice.objects.create(title=title)
                            item_choices.append(choice_obj)

                    if question["type"] == "3":  # 打分题
                        item_choices = models.Choice.objects.filter(id__in=[1, 2, 3, 4, 5])

                    item.choices.add(*item_choices)

                items.append(item)

            survey_obj = models.Survey.objects.create(title=survey_title)
            survey_obj.items.add(*items)
    except Exception as e:
        print(str(e))
        response["status"] = False
        response["msg"] = str(e)

    return HttpResponse(json.dumps(response))
