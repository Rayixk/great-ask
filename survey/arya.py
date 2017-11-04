# Created by yang
from datetime import datetime, timedelta, time
from django.conf.urls import url
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render
from survey.models import SurveyItem
from . import models
from arya.service import sites


class UserInfoConfig(sites.AryaConfig):
    list_display = ['name']


sites.site.register(models.UserInfo, UserInfoConfig)


class SurveyConfig(sites.AryaConfig):
    list_display = ['title']

    def add_view(self, request, *args, **kwargs):
        type_choices = SurveyItem.type_choices
        context = {
            "type_choices": type_choices,
            "url": self.changelist_url,
        }
        print(context)
        return render(request, "add_survey.html", context)


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
    def item_type(self, obj=None, is_header=False):
        if is_header:
            return "类型"

        return obj.get_type_display()

    list_display = ["title", item_type]


sites.site.register(models.SurveyItem, SurveyItemConfig)


class MeetingRoomConfig(sites.AryaConfig):
    # 就在这里做筛选--还是不行

    list_display = ["addr", ]


sites.site.register(models.MeetingRoom, MeetingRoomConfig)


class MeetingRoomDesc(object):
    """封装一个room的描述信息"""

    def __init__(self, room):
        self.room = room
        self.addr = room.addr
        self.pk = room.pk
        self.desc = self.get_desc()

    def get_desc(self):
        res = []
        # s = "%s号(上午,下午)"
        # info={"data":None,"上午":False,"下午":False}
        info = {}
        records = models.MeetingRoomBookList.objects.filter(meeting_room=self.room).order_by("start_time")
        for record in records:
            day = record.start_time.day
            today = record.end_time.date()  # 本处的today指代的是预定记录的当天
            today_12h = datetime.combine(today, time(12, 0))
            today_18h = datetime.combine(today, time(18, 0))
            if record.end_time < today_12h:
                if day not in info:
                    info[day] = {}
                info[day]["上午"] = True
            elif record.end_time < today_18h:
                if day not in info:
                    info[day] = {}
                info[day]["下午"] = True

        for k, v in info.items():
            if len(v) == 2:
                s = "%s号(上午,下午)" % k
                res.append(s)
            else:
                s = "%s号(%s)" % (k, "上午" if "上午" in v else "下午")
                res.append(s)

        if not res:
            return "无"
        elif len(res) > 4:
            res = res[:4]

        return ",".join(res)


class MeetingRoomBook(object):
    """封装book_meeting_room.html页面所需要的数据"""

    def __init__(self):
        self.init_time()
        self.meeting_rooms = self.get_meeting_room()

    def get_meeting_room(self, date=None):
        res = []
        rooms = models.MeetingRoom.objects.all()
        for room in rooms:
            res.append(room)
            # if self.can_be_book(room):
            #     #可以被预定
            #     res.append(room)
            # else:
            #     #不可被预定
            #    pass

        print(res)
        return self.edit_the_desc_info(res)

    def edit_the_desc_info(self, rooms):
        """编辑rooms在页面上显示的信息"""
        res = []
        for room in rooms:
            obj = MeetingRoomDesc(room)
            res.append(obj)
        for i in res:
            print(i.addr, i.desc)
        return res

    def can_be_book(self, room, date=None):
        """判断一个会议室是否能被预定,date为None表示时间范围是5天内"""
        if not date:
            # 没有筛选条件,时间范围是5天
            today = datetime.now().date()  # datetime.datetime(2017, 11, 3)
            next_day1 = today + timedelta(1)
            next_day2 = today + timedelta(2)
            next_day3 = today + timedelta(3)
            next_day4 = today + timedelta(4)
            next_day5 = today + timedelta(5)
            today_start = datetime.combine(today, time())  # datetime.datetime(2017, 11, 3, 0, 0)
            next_day1_start = datetime.combine(next_day1, time())  # datetime.datetime(2017, 11, 4, 0, 0)
            next_day2_start = datetime.combine(next_day2, time())  # datetime.datetime(2017, 11, 5, 0, 0)
            next_day3_start = datetime.combine(next_day3, time())  # datetime.datetime(2017, 11, 6, 0, 0)
            next_day4_start = datetime.combine(next_day4, time())  # datetime.datetime(2017, 11, 7, 0, 0)
            next_day5_start = datetime.combine(next_day5, time())  # datetime.datetime(2017, 11, 8, 0, 0)

            con_date = Q()

            q1 = Q()
            q1.connector = "AND"
            q1.children.append(("start_time__gte", today_start))
            q1.children.append(("start_time__lt", next_day1_start))
            con_date.add(q1, "OR")

            q2 = Q()
            q2.connector = "AND"
            q2.children.append(("start_time__gte", next_day1_start))
            q2.children.append(("start_time__lt", next_day2_start))
            con_date.add(q2, "OR")

            q3 = Q()
            q3.connector = "AND"
            q3.children.append(("start_time__gte", next_day2_start))
            q3.children.append(("start_time__lt", next_day3_start))
            con_date.add(q3, "OR")

            q4 = Q()
            q4.connector = "AND"
            q4.children.append(("start_time__gte", next_day3_start))
            q4.children.append(("start_time__lt", next_day4_start))
            con_date.add(q4, "OR")

            q5 = Q()
            q5connector = "AND"
            q5.children.append(("start_time__gte", next_day4_start))
            q5.children.append(("start_time__lt", next_day5_start))
            con_date.add(q5, "OR")

            # 和room对象相拼接
            room_q = Q()
            room_q.children.append(("meeting_room", room))

            con = Q()
            con.add(room_q, "AND")
            con.add(con_date, "AND")

            objs = models.MeetingRoomBookList.objects.filter(con)
            if objs:
                # 5天内有预定记录
                return False
            else:
                return True

        """
        con = Q()
        for k, v in condition.items():
            tmp = Q()
            tmp.connector = "OR"
            for val in v:
                tmp.children.append((k, val))
        
            con.add(tmp, "AND")

        """






        # if :

    def init_time(self):
        d1 = datetime.now()
        d2 = d1 + timedelta(days=+1)
        d3 = d1 + timedelta(days=+2)
        d4 = d1 + timedelta(days=+3)
        d5 = d1 + timedelta(days=+4)
        setattr(self, "d1", d1.strftime("%Y-%m-%d"))
        setattr(self, "d2", d2.strftime("%Y-%m-%d"))
        setattr(self, "d3", d3.strftime("%Y-%m-%d"))
        setattr(self, "d4", d4.strftime("%Y-%m-%d"))
        setattr(self, "d5", d5.strftime("%Y-%m-%d"))


class MeetingRoomBookListConfig(sites.AryaConfig):
    def start_time(self, obj=None, is_header=False):
        if is_header:
            return "开始时间"
        return obj.start_time.strftime("%Y-%m-%d %H:%M")

    def end_time(self, obj=None, is_header=False):
        if is_header:
            return "结束时间"
        return obj.end_time.strftime("%Y-%m-%d %H:%M")

    def meetingroom_book(self, request, *args, **kwargs):
        book_info_obj = MeetingRoomBook()
        context = {
            "book_info_obj": book_info_obj
        }
        return render(request, "book_meeting_room.html", context)

    def extra_urls(self):
        app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        the_url = url(r'^meetingroom_book$', self.wrapper(self.meetingroom_book),
                      name="%s_%s_meetingroom_book" % app_model_name)
        return [the_url, ]

    list_display = ["meeting_room", start_time, end_time, "theme", "user"]


sites.site.register(models.MeetingRoomBookList, MeetingRoomBookListConfig)
