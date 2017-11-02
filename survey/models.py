from django.db import models
from rbac.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(to=User, verbose_name="用户账号")
    name = models.CharField("姓名", max_length=32)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(to="UserInfo", verbose_name="学生姓名")
    class_list = models.ManyToManyField(to="ClassList", verbose_name="以报班级")

    def __str__(self):
        return self.user.name


class ClassList(models.Model):
    """班级"""
    name = models.CharField("班级名称", max_length=32)

    def __str__(self):
        return self.name


class Survey(models.Model):
    title = models.CharField("问卷名称", max_length=128)
    date = models.DateField("创建日期", auto_now_add=True)
    # class_list = models.ManyToManyField(to="ClassList", verbose_name="所属班级") 此字段废掉,一份问卷都可填写
    items = models.ManyToManyField(to="SurveyItem",verbose_name="题目")

    def __str__(self):
        return self.title


class SurveyItem(models.Model):
    title = models.CharField("问题", max_length=32)
    type_choices = [
        (1, "单选"),
        (2, "多选"),
        (3, "打分题"),
        (4, "text"),
        (5, "text-area"),
    ]
    type = models.SmallIntegerField("类型", choices=type_choices, default=1)
    choices = models.ManyToManyField(to="Choice", verbose_name="选项")


class Choice(models.Model):
    title = models.CharField("选项名称", max_length=128)

    def __str__(self):
        return self.title


class InputRecord(models.Model):
    """填空题记录表"""
    user = models.ForeignKey(to="Student", verbose_name="用户")
    question = models.ForeignKey(to="SurveyItem", verbose_name="问题")
    answer = models.CharField("答案", max_length=512)


class ChoiceRecord(models.Model):
    """选择题记录表"""
    user = models.ForeignKey(to="Student", verbose_name="用户")
    question = models.ForeignKey(to="SurveyItem", verbose_name="问题")
    answer = models.ForeignKey(to="Choice", verbose_name="答案")


class MeetingRoom(models.Model):
    """会议室"""
    addr = models.CharField("会议室地点", max_length=32)


class MeetingRoomBookList(models.Model):
    """会议室预定记录表"""
    meeting_room = models.ForeignKey(to='MeetingRoom', verbose_name='会议室')
    start_time = models.DateTimeField("开始时间")
    end_time = models.DateTimeField("结束时间")
    for_who = models.ForeignKey(to="UserInfo", verbose_name="为谁预定")
