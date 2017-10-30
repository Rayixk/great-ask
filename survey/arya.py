# Created by yang

from . import models
from arya.service import sites

class UserInfoConfig(sites.AryaConfig):
    list_display = ['name']
sites.site.register(models.UserInfo,UserInfoConfig)

class SurveyConfig(sites.AryaConfig):
    list_display = ['title']

sites.site.register(models.Survey,SurveyConfig)

class ChoiceBoxConfig(sites.AryaConfig):
    list_display = ['title']
sites.site.register(models.ChoiceBox,ChoiceBoxConfig)

class InputBoxConfig(sites.AryaConfig):
    list_display = ['title']
sites.site.register(models.InputBox,InputBoxConfig)

class TextAreaConfig(sites.AryaConfig):
    list_display = ['title']
sites.site.register(models.TextArea,TextAreaConfig)

class ChoiceConfig(sites.AryaConfig):
    def choice_box(self,obj=None, is_header=False):
        if is_header:
            return "所属问题"
        return "{}({})".format(obj.choice_box.title,obj.choice_box.survey.title)

    def status(self,obj=None, is_header=False):
        if is_header:
            return "是否选中"
        return obj.get_status_display()

    list_display = [choice_box,"title",status]
sites.site.register(models.Choice,ChoiceConfig)
