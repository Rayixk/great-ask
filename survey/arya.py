# Created by yang

from . import models
from arya.service import sites


class UserInfoConfig(sites.AryaConfig):
    list_display = ['name']


sites.site.register(models.UserInfo, UserInfoConfig)


class SurveyConfig(sites.AryaConfig):
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
