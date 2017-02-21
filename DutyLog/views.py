#coding=utf-8

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

from django.shortcuts import render
from .models import DutyInfo, ContentTable, InstructionTable, ResultTable, ProxyInstructionTable, RoleTable
from django.utils import timezone
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

#@login_required
def index(request):
    roleflag = request.GET.get("roleflag")
    dutyinfo_exist_flag = "false"  # 值班信息是否已经存在标志
    page_no = request.GET.get("page_no")
    # 用户信息
    proxy_user_list = RoleTable.objects.filter(roleflag='3')  # 带班领导
    leader_user_list = RoleTable.objects.filter(roleflag='2')  # 值班领导
    man_user_list = RoleTable.objects.filter(roleflag='1')  # 值班员
    manager_user_list = RoleTable.objects.filter(roleflag='4')  # 值班科长
    date_and_time = datetime.now()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[datetime.today().weekday()]
    dutyinfo_obj = None
    if not page_no:
        date_str = str(datetime.now())[:10]
        try:
            dutyinfo_obj = DutyInfo.objects.get(date=date_str)
        except:
            pass
        if dutyinfo_obj:#如果能找到，说明已经存在，查找页码
            page_no = dutyinfo_obj.page_no
            dutyinfo_exist_flag = "true"
        else:
            dutyinfo_obj_list = DutyInfo.objects.order_by('-page_no')
            if dutyinfo_obj_list:
                biggest_page_no = dutyinfo_obj_list[0].page_no
                page_no = biggest_page_no + 1
            else:
                page_no = 1
    else:
        pass
    try:
        dutyinfo_obj = DutyInfo.objects.get(page_no=page_no)  # 值班员信息
        dutyinfo_exist_flag = "true"
    except:
        dutyinfo_obj = None
    try:
        content_obj = ContentTable.objects.get(page_no=page_no) #内容信息
    except:
        content_obj = None
    try:
        instruction_obj = InstructionTable.objects.get(page_no=page_no)  # 值班领导信息
    except:
        instruction_obj = None
    try:
        proxy_instruction_obj = ProxyInstructionTable.objects.get(page_no=page_no)  # 代班领导信息
    except:
        proxy_instruction_obj = None
    try:
        result_obj = ResultTable.objects.get(page_no=page_no)  # result信息
    except:
        result_obj = None


    context = {"dutyinfo": dutyinfo_obj, "content": content_obj, "instruction_obj": instruction_obj, "page_no": page_no, "dutyinfo_exist_flag": dutyinfo_exist_flag,
               "proxy_instruction_obj": proxy_instruction_obj, "result_obj": result_obj, "roleflag": roleflag,  "date_and_time":date_and_time, "weekday":weekday,
               "proxy_user_list": proxy_user_list, "manager_user_list": manager_user_list, "man_user_list": man_user_list, "leader_user_list": leader_user_list}

    return render(request, "DutyLog/index.html", context)

@csrf_exempt
def log_handler(request):
    flag = request.POST.get("flag")  #
    time_now = datetime.now()
    page_no = request.POST.get("page_no")

    if flag == "1":   #值班员点击content按钮
        content = request.POST.get("content")
        try:
            content_obj = ContentTable.objects.get(page_no = page_no)
        except:
            content_obj = None
        if content_obj: #已存在
            id = content_obj.id
            content_obj = ContentTable(id=id, content=content, content_time=content_obj.content_time, modify_time=time_now, page_no=page_no)
        else: #不存在
            content_obj = ContentTable(content=content, content_time=time_now,
                                       modify_time=time_now, page_no=page_no)
        content_obj.save()
        return JsonResponse({"status": "ok"})
    if flag == "2": #值班领导
        proxy_instruction = request.POST.get("proxy_instruction")
        try:
            proxy_instruction_obj = ProxyInstructionTable.objects.get(page_no=page_no)
        except:
            proxy_instruction_obj = None
        if proxy_instruction_obj:
            id = proxy_instruction_obj.id
            proxy_instruction_obj = ProxyInstructionTable(id=id, page_no=page_no, proxy_instruction=proxy_instruction,
                                                          proxy_instruction_time=time_now, modify_time=time_now)
        else:
            proxy_instruction_obj = ProxyInstructionTable(page_no=page_no, proxy_instruction=proxy_instruction, proxy_instruction_time=time_now, modify_time=time_now)
        proxy_instruction_obj.save()
        return JsonResponse({"status": "ok"})
    if flag == "3": #带班领导
        instruction = request.POST.get("instruction")
        try:
            instruction_obj = InstructionTable.objects.get(page_no=page_no)
        except:
            instruction_obj = None
        if instruction_obj:
            id = instruction_obj.id
            instruction_obj = InstructionTable(id=id, page_no=page_no, instruction=instruction, instruction_time=time_now,
                                               modify_time=time_now)
        else:
            instruction_obj = InstructionTable(page_no=page_no, instruction=instruction, instruction_time=time_now, modify_time=time_now)
        instruction_obj.save()
        return JsonResponse({"status": "ok"})
    if flag == "4": #办理结果，值班员填写
        result = request.POST.get("result")
        try:
            request_obj = ResultTable.objects.get(page_no=page_no)
        except:
            request_obj = None
        if request_obj:
            id = request_obj.id
            result_obj = ResultTable(id=id, page_no=page_no, result=result, result_time=time_now, modify_time=time_now)
        else:
            result_obj = ResultTable(page_no=page_no, result=result, result_time=time_now, modify_time=time_now)
        result_obj.save()
        return JsonResponse({"status": "ok"})


def myadmin(request):
    user_list = RoleTable.objects.order_by('username')
    context = {"user_list": user_list}
    return render(request, "DutyLog/myadmin.html", context)

@csrf_exempt
#@login_required
def adduser(request):
    if request.method == "GET":
        return render(request, "DutyLog/adduser.html")
    if request.method == "POST":  # roleflag 1为值班员, 2为值班领导，3为带班领导 4，值班科长
        username = request.POST.get("username")
        password = request.POST.get("password")
        roleflag = request.POST.get("roleflag")
        #找出当前数据库中的所有的用户名，如果username已经存在，不允许增加用户，返回错误信息
        user_list = RoleTable.objects.order_by('username')
        username_list = [user.username for user in user_list]
        if username in username_list:
            return JsonResponse({"status": "用户已存在"})
        roletable_obj = RoleTable(username=username, password=password, roleflag=roleflag)
        roletable_obj.save()
        return JsonResponse({"status": "增加成功"})

@csrf_exempt
def myadmin_login(request):#用户登陆后的处理页面
    status = "error"
    msg = ""
    roleflag = "0"
    username = request.POST.get("username")
    password = request.POST.get("password")
    user_list = RoleTable.objects.order_by("username")
    username_list = [user.username for user in user_list]
    if username in username_list:
        user_obj = RoleTable.objects.get(username = username)
        if password == user_obj.password: #登陆成功
            status = "ok"
            msg = "登陆成功"
            roleflag = user_obj.roleflag
        else:
            status = "error"
            msg = "兄台，密码错了"
    else:
        status = "error"
        msg = "密码错误"
    res = {"status": status, "msg": msg,"roleflag": roleflag}
    return JsonResponse(res)

def archive(request):  #归档
    dutyinfo_list = DutyInfo.objects.order_by("-date")
    context = {"dutyinfo_list": dutyinfo_list}
    return render(request, "DutyLog/archive.html", context)

@csrf_exempt
def sign_in(request):  #值班员签到
    time_now = datetime.now()
    page_no = request.POST.get("page_no")
    duty_leader = request.POST.get("duty_leader").encode('utf8')
    duty_man = request.POST.get("duty_man")
    duty_manager = request.POST.get("duty_manager")
    duty_proxy = request.POST.get("duty_proxy")
    date = request.POST.get("date")
    # weekday = request.POST.get("weekday")
    weather = request.POST.get("weather")
    temp = request.POST.get("temp")
    # 获取星期
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[datetime.today().weekday()]
    # 判断当前page_no是否已经存在对应的信息，如果不存在，则新增，存在则更新
    try:
        dutyinfo_obj = DutyInfo.objects.get(page_no=page_no)
    except:
        dutyinfo_obj = None
    if dutyinfo_obj:  # 已存在
        id = dutyinfo_obj.id
        dutyinfo_obj = DutyInfo(id=id, duty_time=dutyinfo_obj.duty_time, page_no=page_no, duty_leader=duty_leader,
                                duty_man=duty_man,
                                duty_manager=duty_manager, duty_proxy=duty_proxy,
                                date=date, weekday=dutyinfo_obj.weekday, weather=weather, temp=temp)
    else:  # 不存在
        dutyinfo_obj = DutyInfo(page_no=page_no, duty_time=time_now, duty_leader=duty_leader, duty_man=duty_man,
                                duty_manager=duty_manager, duty_proxy=duty_proxy,
                                date=date, weekday=weekday, weather=weather, temp=temp)
    dutyinfo_obj.save()
    return JsonResponse({"status": u"您今日签到成功"})

# 是否允许新增,根据日期从数据库中查找dutyinfo，如果能找到，说明存在，不允许新增，否则允许新增
def get_sign_in_flag(request):
    date = request.GET.get("date")
    sign_in_flag = "true"  #默认允许签到
    dutyinfo_obj = None
    try:
        dutyinfo_obj = DutyInfo.objects.get(date=date)
    except:
        pass
    if dutyinfo_obj:
        sign_in_flag = "false"  #如果已经存在，不允许签到
    return JsonResponse({"sign_in_flag": sign_in_flag})

def search(request):
    keyword = request.GET.get("keyword")
    if keyword:
        sql = "SELECT * FROM DutyLog_contenttable WHERE content LIKE '%%" + keyword + "%%'"
        content_list = ContentTable.objects.raw(sql)
        if content_list:
            page_no_list = [content.page_no for content in content_list]
            return JsonResponse({"status": "ok","page_no_list": page_no_list})
        return JsonResponse({"status": "error"})
    return render(request, "Dutylog/search.html")

def get_dutyinfo_by_page_no(request):
    page_no = request.GET.get("page_no")
    if page_no:
        dutyinfo = DutyInfo.objects.get(page_no=page_no)
        res = {"status": "ok", "date": dutyinfo.date, "weekday": dutyinfo.weekday, "duty_man": dutyinfo.duty_man, "duty_leader":dutyinfo.duty_leader,
               "duty_manager": dutyinfo.duty_manager, "duty_proxy": dutyinfo.duty_proxy, "weather": dutyinfo.weather, "temp": dutyinfo.temp, "page_no": dutyinfo.page_no}
        return JsonResponse(res)
    return JsonResponse({"status": "error"})




