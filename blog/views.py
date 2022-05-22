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
    # print('===========in func login', request)
    if request.method == 'POST':
        userform = UserFormLogin(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user = None
            try:
                user = User.objects.raw('select * from blog_user where blog_user.name = %s', [username])[0]
            except:
                script = 'alert'
                message = '用户名不存在'
                return render(request, 'login.html', locals())
            if user.password == password:
                global username_global
                username_global = username
                request.session['self_script'] = 'alert'
                request.session['self_message'] = '登录成功'
                return redirect('/blog/index/')
            else:
                script = 'alert'
                message = '用户名或密码错误'
                return render(request, 'login.html', locals())
    else:
        script = request.session.get('self_script')
        message = request.session.get('self_message')
        request.session['self_script'] = None
        request.session['self_message'] = None
        userform = UserFormLogin()
    return render(request, 'login.html', locals())


@identity_check
def index(request):
    # print('===========in index')
    username = username_global

    script = request.session.get('self_script')
    message = request.session.get('self_message')
    request.session['self_script'] = None
    request.session['self_message'] = None

    # 我关注的人数
    follow_me_list = Follow.objects.raw('select * from blog_follow where following_id = %s', [username])
    follow_me_list_len = len(follow_me_list)

    # 关注我的人数
    my_follow_list = Follow.objects.raw('select * from blog_follow where be_followed_id = %s', [username])
    my_follow_list_len = len(my_follow_list)

    # 展示关注人的帖子
    cursor = connection.cursor()
    cursor.execute('select blog_post.id, blog_post.author_id, blog_post.content, blog_post.time, likenum from post_id_likenum, blog_post, blog_follow where blog_follow.following_id = %s and blog_follow.be_followed_id = blog_post.author_id and post_id_likenum.id = blog_post.id;', [username])
    follow_post_list = list(cursor.fetchall())[::-1]
    print(follow_post_list)
    cursor.close()

    searchform = SearchForm(request.POST)
    if request.method == 'POST':
        if searchform.is_valid():
            search_name = searchform.cleaned_data['search_name']
            search_name = "%"+search_name+"%"
            users_list = User.objects.raw('select * from blog_user where blog_user.name like %s', [search_name])
            return render(request, 'index.html', locals())
    else:
        return render(request, 'index.html', locals())


@identity_check
def userinfo(request):
    # print('===========in userinfo')
    hisname = request.GET.get('info')
    username = username_global
    script = request.session.get('self_script')
    message = request.session.get('self_message')
    request.session['self_script'] = None
    request.session['self_message'] = None

    # 我有没有关注他
    follow_list = Follow.objects.raw('select * from blog_follow where following_id = %s and be_followed_id = %s', [username, hisname])

    # 查看他的发帖
    cursor = connection.cursor()
    cursor.execute('select blog_post.id, blog_post.author_id, blog_post.content, blog_post.time, likenum from post_id_likenum, blog_post where blog_post.author_id = %s and post_id_likenum.id = blog_post.id', [hisname])
    post_list = list(cursor.fetchall())[::-1]
    cursor.close()
   
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
    # print('===========in post')
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


@identity_check
def follow(request):
    # print('===========in follow')
    username = username_global
    hisname = request.GET.get('goal')
    # 不用检查是否已关注，直接insert即可（在前面做检查了）
    # 但是最好再加一个except
    cursor = connection.cursor()
    try:
        cursor.execute(f'insert into blog_follow value(DEFAULT, \'{hisname}\', \'{username}\')')
    except:
        request.session['self_script'] = 'alert'
        request.session['self_message'] = '关注失败，出现了奇怪的错误'
        return redirect(f'/blog/userinfo/?info={hisname}')
    request.session['self_script'] = 'alert'
    request.session['self_message'] = '关注成功'
    return redirect(f'/blog/userinfo/?info={hisname}')


@identity_check
def unfollow(request):
    # print('===========in unfollow')
    username = username_global
    hisname = request.GET.get('goal')
    # 不用检查是否已关注，直接delete即可（在前面做检查了）
    # 但是最好再加一个except
    cursor = connection.cursor()
    try:
        cursor.execute('delete from blog_follow where following_id = %s and be_followed_id = %s', [username, hisname])
    except:
        request.session['self_script'] = 'alert'
        request.session['self_message'] = '取关失败，出现了奇怪的错误'
        return redirect(f'/blog/userinfo/?info={hisname}')
    request.session['self_script'] = 'alert'
    request.session['self_message'] = '取消关注成功'
    return redirect(f'/blog/userinfo/?info={hisname}')


@identity_check
def like(request):
    post_id = request.GET.get('id')
    hisname = Post.objects.raw('select * from blog_post where blog_post.id = %s', [post_id])[0].author_id
    source = request.GET.get('from')
    username = username_global
    cursor = connection.cursor()
    try:
        cursor.execute(f'insert into blog_like value(DEFAULT, \'{post_id}\', \'{username}\')')
    except:
        request.session['self_script'] = 'alert'
        request.session['self_message'] = '点赞失败，出现了奇怪的错误'
    finally:
        cursor.close()
    
    if source == 'index':
        return redirect('/blog/index/')
    elif source == 'info':
        return redirect(f'/blog/userinfo/?info={hisname}')


@identity_check
def logout(request):
    # print('===========in logout')
    global username_global
    username_global = None
    return redirect(f'/blog/login/')