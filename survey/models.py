from django.db import models
from rbac.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(to=User, verbose_name="用户账号")
    name = models.CharField("姓名", max_length=32)

    def __str__(self):
        return self.name


class Survey(models.Model):
    title = models.CharField("问卷名称", max_length=128)
    date = models.DateField("创建日期", auto_now_add=True)
    choice_boxes = models.ManyToManyField(to="ChoiceBox", verbose_name="选择题")
    input_boxes = models.ManyToManyField(to="InputBox", verbose_name="填空题")

    def __str__(self):
        return self.title


class ChoiceBox(models.Model):
    title = models.CharField("问题名称", max_length=128)
    type_choices = [
        (1, "单选"),
        (2, "多选"),
    ]
    type = models.SmallIntegerField("选择题类型", choices=type_choices, default=1)
    choices = models.ManyToManyField(to="Choice",verbose_name="选项")

    def __str__(self):
        return self.title


class InputBox(models.Model):
    title = models.CharField("问题名称", max_length=128)
    type_choices = [
        (1, "text"),
        (2, "text-area"),
    ]
    type = models.SmallIntegerField("填空题类型", choices=type_choices, default=1)

    def __str__(self):
        return self.title


class Choice(models.Model):
    title = models.CharField("选项名称", max_length=128)

    def __str__(self):
        return self.title


class InputRecord(models.Model):
    """填空题记录表"""
    user = models.ForeignKey(to="UserInfo", verbose_name="用户")
    survey = models.ForeignKey(to="Survey", verbose_name="问卷")
    question = models.ForeignKey(to="InputBox", verbose_name="问题")
    answer = models.CharField("答案", max_length=512)


class ChoiceRecord(models.Model):
    """选择题记录表"""
    user = models.ForeignKey(to="UserInfo", verbose_name="用户")
    survey = models.ForeignKey(to="Survey", verbose_name="问卷")
    question = models.ForeignKey(to="ChoiceBox", verbose_name="问题")
    answer = models.ForeignKey(to="Choice")
