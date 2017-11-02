# Created by yang
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse,render

from . import models
from arya.service import sites


class UserInfoConfig(sites.AryaConfig):
    list_display = ['name']


sites.site.register(models.UserInfo, UserInfoConfig)


class SurveyConfig(sites.AryaConfig):
    list_display = ['title']

    def add_view(self, request, *args, **kwargs):
        return render(request,"add_survey.html")


sites.site.register(models.Survey, SurveyConfig)


class ChoiceConfig(sites.AryaConfig):
    list_display = ["title"]


sites.site.register(models.Choice, ChoiceConfig)


class InputRecordConfig(sites.AryaConfig):
    list_display = ["user", "question", "answer"]


sites.site.register(models.InputRecord, InputRecordConfig)


class ChoiceRecordConfig(sites.AryaConfig):
    list_display = ["user", "question", "answer"]


sites.site.register(models.ChoiceRecord, ChoiceRecordConfig)


class ClassListConfig(sites.AryaConfig):
    list_display = ["name", ]


sites.site.register(models.ClassList, ClassListConfig)


class StudentConfig(sites.AryaConfig):
    def class_list(self, obj=None, is_header=False):
        if is_header:
            return '以报班级'
        classes = obj.class_list.all()
        result = []
        for class_obj in classes:
            tpl = "<span>{}</span>".format(class_obj.name)
            result.append(tpl)
        return mark_safe(" ".join(result))

    list_display = ["user", class_list]


sites.site.register(models.Student, StudentConfig)


class InputRecordConfig(sites.AryaConfig):
    list_display = ["user", "question", "answer"]


sites.site.register(models.InputRecord, InputRecordConfig)


class ChoiceRecordConfig(sites.AryaConfig):
    list_display = ["user", "question", "answer"]


sites.site.register(models.ChoiceRecord, ChoiceRecordConfig)


class SurveyItemConfig(sites.AryaConfig):

    def item_type(self,obj=None,is_header=False):
        if is_header:
            return "类型"

        return obj.get_type_display()

    list_display = ["title",item_type]


sites.site.register(models.SurveyItem, SurveyItemConfig)
