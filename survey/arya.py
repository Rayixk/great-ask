# Created by yang
from django.utils.safestring import mark_safe

from . import models
from arya.service import sites


class UserInfoConfig(sites.AryaConfig):
    list_display = ['name']


sites.site.register(models.UserInfo, UserInfoConfig)


class SurveyConfig(sites.AryaConfig):
    # def generate_survey(self, request):
    #
    #     pass
    #
    # generate_survey.short_description = "生成问卷"
    # actions = [generate_survey,]

    def generate_survey(self):
        from django.shortcuts import HttpResponse
        return HttpResponse("xxxxxx")

    def extra_urls(self):
        from django.conf.urls import url
        patterns = [
            url(r'^generate_survey$', SurveyConfig.generate_survey)
        ]

        return patterns

    list_display = ['title']


sites.site.register(models.Survey, SurveyConfig)


class ChoiceBoxConfig(sites.AryaConfig):
    list_display = ['title']


sites.site.register(models.ChoiceBox, ChoiceBoxConfig)


class InputBoxConfig(sites.AryaConfig):
    list_display = ['title']


sites.site.register(models.InputBox, InputBoxConfig)


class ChoiceConfig(sites.AryaConfig):
    list_display = ["title"]


sites.site.register(models.Choice, ChoiceConfig)


class InputRecordConfig(sites.AryaConfig):
    list_display = ["user", "survey", "question", "answer"]


sites.site.register(models.InputRecord, InputRecordConfig)


class ChoiceRecordConfig(sites.AryaConfig):
    list_display = ["user", "survey", "question", "answer"]


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
    list_display = ["user","survey", "question", "answer"]


sites.site.register(models.InputRecord, InputRecordConfig)


class ChoiceRecordConfig(sites.AryaConfig):
    list_display = ["user", "survey", "question", "answer"]


sites.site.register(models.ChoiceRecord, ChoiceRecordConfig)
