from django.http import HttpResponse
import json
from django import forms
from .models import *
from hashlib import sha1



def index(request):
    return HttpResponse("Hello, I am Jin Bao.")


# 注册
def sign_up(request):
    if request.method == 'POST':
        # 获取表单
        try:
            form = forms.Form(request.POST)
            username = form.data['username']
            password = form.data['password']
            identity = form.data['identity']
            print(password)
        except:
            resp = {'Status': 'ERROR', 'detail': 'Valid form needed'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 合法性检查
        if len(identity) * len(password) * len(username) == 0:
            resp = {'Status': 'ERROR', 'detail': 'All blanks should be filled'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        if User.objects.filter(username=username).count() != 0:
            resp = {'Status': 'ERROR', 'detail': 'Username has been used'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        obj = User.objects.create(username=username, password=sha1(password.encode('utf-8')).hexdigest(), identity=identity)
        obj.save()

        resp = {'Status': 'SUCCESS'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp = {'Status': 'ERROR', 'detail': 'Use POST to access this page'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


# 登录
def sign_in(request):
    if request.method == 'POST':
        # 获取表单
        try:
            form = forms.Form(request.POST)
            username = form.data['username']
            password = form.data['password']
            print(password)
        except:
            resp = {'Status': 'ERROR', 'detail': 'Valid form needed'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 检查用户名是否存在
        if User.objects.filter(username=username).count() == 0:
            resp = {'Status': 'ERROR', 'detail': 'Username not found'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        user = User.objects.get(username=username)

        # 校验密码
        print(sha1(password.encode('utf-8')).hexdigest())
        print(user.password)
        if sha1(password.encode('utf-8')).hexdigest() != user.password:
            resp = {'Status': 'ERROR', 'detail': 'Wrong password'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 用户名保存到session方便将来使用
        request.session['username'] = username

        resp = {'Status': 'SUCCESS'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp = {'Status': 'ERROR', 'detail': 'Use POST to access this page'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

# 列出所有课程和用户已修课程
def display(request):
    try:
        username = request.session['username']
    except:
        resp = {'Status': 'ERROR', 'detail': 'Sign in first'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    # 获取全部课程
    courses = Course.objects.all()
    resp = []
    for i in courses:
        resp.append({'name':i.name, 'grade':i.grade, 'former':i.former})

    # 获取已修课程
    user = User.objects.get(username=username)
    for i in user.learned_courses.all():
        resp.append({'learned_course':i.name})

    # 获取已选课程
    for i in user.chosen_courses.all():
        resp.append({'chosen_course': i.name})
    return HttpResponse(json.dumps(resp), content_type="application/json")

def pick(request):
    try:
        username = request.session['username']
    except:
        resp = {'Status': 'ERROR', 'detail': 'Sign in first'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


    if request.method == 'POST':
        # 获取表单
        try:
            form = forms.Form(request.POST)
            id = form.data['id']
        except:
            resp = {'Status': 'ERROR', 'detail': 'Valid form needed'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        user = User.objects.get(username=username)

        # 合法性检查
        if Course.objects.filter(id=id).count() == 0:
            resp = {'Status': 'ERROR', 'detail': 'Course not found'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        course = Course.objects.get(id=id)
        if course.grade != user.grade:
            resp = {'Status': 'ERROR', 'detail': 'Grade doesnt match'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        if course.former:
            if not set(course.former) < set(user.learned_courses.all()):
                resp = {'Status': 'ERROR', 'detail': 'Learn former courses needed'}
                return HttpResponse(json.dumps(resp), content_type="application/json")

        # 选课
        user.chosen_courses.add(course)

        resp = {'Status': 'SUCCESS'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp = {'Status': 'ERROR', 'detail': 'Use POST to access this page'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

# 撤课
def delete(request):
    try:
        username = request.session['username']
    except:
        resp = {'Status': 'ERROR', 'detail': 'Sign in first'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


    if request.method == 'POST':
        # 获取表单
        try:
            form = forms.Form(request.POST)
            id = form.data['id']
        except:
            resp = {'Status': 'ERROR', 'detail': 'Valid form needed'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        user = User.objects.get(username=username)

        # 合法性检查
        if user.chosen_courses.filter(id=id).count() == 0:
            resp = {'Status': 'ERROR', 'detail': 'Havent picked the course'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 撤课
        course = user.chosen_courses.get(id=id)
        user.chosen_courses.remove(course)

        resp = {'Status': 'SUCCESS'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp = {'Status': 'ERROR', 'detail': 'Use POST to access this page'}
        return HttpResponse(json.dumps(resp), content_type="application/json")