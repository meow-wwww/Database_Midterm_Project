from django.shortcuts import render, redirect
from django import forms
from .models import *
from django.db import connection,transaction
from django.http import HttpResponse, HttpResponseRedirect

global username_global
username_global = None

# 表单
class UserFormRegister(forms.Form):
    username = forms.CharField(label='用户名',max_length=20)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')

class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名',max_length=20)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

class SearchForm(forms.Form):
    search_name = forms.CharField(label='想查找的用户名',max_length=20)

class PostForm(forms.Form):
    content = forms.CharField(label='发帖', max_length=180)


# Create your views here.
def identity_check(func):
    def inner(request):
        global username_global
        if username_global == None:
            return redirect('/blog/login/')
        else:
            return func(request)
    return inner


def register(request):
    if request.method == 'POST':
        userform = UserFormRegister(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']

            # 修改数据库
            cursor = connection.cursor()
            try:
                cursor.execute(f'insert into blog_user value(\'{username}\', \'{password}\', \'{email}\')')
            except:
                script = 'alert'
                message = '用户名重复'
                return render(request, 'register.html', locals())
            request.session['self_script'] = 'alert'
            request.session['self_message'] = '注册成功'
            return redirect('/blog/login/')
    else:
        userform = UserFormRegister()
    return render(request, 'register.html', locals())


def login(request):
    print('===========in func login', request)
    if request.method == 'POST':
        userform = UserFormLogin(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user = User.objects.raw('select * from blog_user where blog_user.name = %s', [username])[0]
            if user.password == password:
                global username_global
                username_global = username
                request.session['self_script'] = 'alert'
                request.session['self_message'] = '登录成功'
                return redirect('/blog/index/')
            else:
                script = 'alert'
                message = '用户名或密码错误'
                render(request, 'login.html', locals())
    else:
        script = request.session.get('self_script')
        message = request.session.get('self_message')
        request.session['self_script'] = None
        request.session['self_message'] = None
        userform = UserFormLogin()
    return render(request, 'login.html', locals())


@identity_check
def index(request):
    print('===========in index')
    username = username_global
    script = request.session.get('self_script')
    message = request.session.get('self_message')
    request.session['self_script'] = None
    request.session['self_message'] = None
    searchform = SearchForm(request.POST)
    if request.method == 'POST':
        if searchform.is_valid():
            # print('===========is searching friends')
            search_name = searchform.cleaned_data['search_name']
            search_name = "%"+search_name+"%"
            users_list = User.objects.raw('select * from blog_user where blog_user.name like %s', [search_name])
            return render(request, 'index.html', locals())
    else:
        return render(request, 'index.html', locals())


@identity_check
def userinfo(request):
    print('===========in userinfo')
    username = username_global
    script = request.session.get('self_script')
    message = request.session.get('self_message')
    request.session['self_script'] = None
    request.session['self_message'] = None

    # if request.method == 'POST':
    #     if searchform.is_valid():
    #         # print('===========is searching friends')
    #         search_name = searchform.cleaned_data['search_name']
    #         search_name = "%"+search_name+"%"
    #         users_list = User.objects.raw('select * from blog_user where blog_user.name like %s', [search_name])
    #         return render(request, 'index.html', locals())
    # else:
    return render(request, 'userinfo.html', locals())

@identity_check
def post(request):
    print('===========in post')
    username = username_global
    post_form = PostForm(request.POST)

    if request.method == 'POST':
        if post_form.is_valid():
            content = post_form.cleaned_data['content']
            # 修改数据库
            cursor = connection.cursor()
            try:
                cursor.execute(f'insert into blog_post value(DEFAULT, \'{content}\', \'{datetime.now()}\', \'{username}\')')
            except:
                script = 'alert'
                message = '发送失败'
                return render(request, 'post.html', locals())
            request.session['self_script'] = 'alert'
            request.session['self_message'] = '发送成功'
            return redirect('/blog/index/')
    else:
        return render(request, 'post.html', locals())