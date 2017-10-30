from django.db import models
from rbac.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(to=User,verbose_name="用户账号")
    name = models.CharField("姓名", max_length=32)

    def __str__(self):
        return self.name


class Survey(models.Model):
    title = models.CharField("问卷名称", max_length=128)
    date = models.DateTimeField("创建日期", auto_created=True)

    def __str__(self):
        return self.title


class ChoiceBox(models.Model):
    title = models.CharField("问题名称", max_length=128)
    survey = models.ForeignKey(to="Survey", verbose_name="所属问卷")
    type_choices = [
        (1, "单选"),
        (2, "多选"),
    ]
    type = models.SmallIntegerField("选项类型", choices=type_choices, default=1)

    def __str__(self):
        return self.title


class InputBox(models.Model):
    title = models.CharField("问题名称", max_length=128)
    answer = models.CharField("答案", max_length=200, null=True, blank=True)
    survey = models.ForeignKey(to="Survey", verbose_name="所属问卷")

    def __str__(self):
        return self.title


class TextArea(models.Model):
    title = models.CharField("问题名称", max_length=128)
    answer = models.TextField("答案", max_length=200, null=True, blank=True)
    survey = models.ForeignKey(to="Survey", verbose_name="所属问卷")

    def __str__(self):
        return self.title


class Choice(models.Model):
    title = models.CharField("选项名称", max_length=128)
    is_checked = models.BooleanField("是否选中", default=False)
    choice_box = models.ForeignKey(to="ChoiceBox", verbose_name="所属问题")

    def __str__(self):
        return self.title
