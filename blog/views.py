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
                cursor.execute('insert into blog_user value(%s, %s, %s)', [username, password, email])
            except:
                script = 'alert'
                message = '用户名重复'
                return render(request, 'register.html', locals())
            cursor.close()
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

    # 点赞通知
    cursor = connection.cursor()
    cursor.execute('select * from who_likes_me where who_likes_me.author_id = %s and who_likes_me.read = 0',[username])
    like_notify_list = list(cursor.fetchall())
    like_notify_list.sort(key=lambda x:x[0])
    like_notify_list = like_notify_list[::-1]
    cursor.close()
    like_notify_list_len = len(like_notify_list)

    # 展示关注人的帖子
    cursor = connection.cursor()
    cursor.execute('select id, author, content, time, likenum, like_or_not from my_follow_post_bool where my_follow_post_bool.myid = %s', [username])
    follow_post_list = list(cursor.fetchall())
    follow_post_list.sort(key=lambda x:x[0])
    follow_post_list = follow_post_list[::-1]
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
def myfollow(request):
    username = username_global
    # 我关注的人数
    follow_me_list = Follow.objects.raw('select * from blog_follow where following_id = %s', [username])
    follow_me_list_len = len(follow_me_list)
    # for i in follow_me_list:
        # print(i.name)
    return render(request, 'myfollow.html', locals())


@identity_check
def followme(request):
    username = username_global
    # 关注我的人数
    my_follow_list = Follow.objects.raw('select * from blog_follow where be_followed_id = %s', [username])
    my_follow_list_len = len(my_follow_list)
    return render(request, 'followme.html', locals())


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
    cursor.execute('select id, author, content, time, likenum, like_or_not from ones_post_bool where ones_post_bool.myid = %s and ones_post_bool.hisid = %s', [username, hisname])
    post_list = list(cursor.fetchall())
    post_list.sort(key=lambda x:x[0])
    post_list = post_list[::-1]
    # print(post_list)
    cursor.close()
   
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
                cursor.execute(f'insert into blog_post value(DEFAULT, %s, %s, %s)', [content, datetime.now(), username])
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
        cursor.execute(f'insert into blog_follow value(DEFAULT, %s, %s)', [hisname, username])
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
    cursor.close()
    request.session['self_script'] = 'alert'
    request.session['self_message'] = '取消关注成功'
    return redirect(f'/blog/userinfo/?info={hisname}')


@identity_check
def like(request):
    post_id = request.GET.get('id')
    hisname = Post.objects.raw('select * from blog_post where blog_post.id = %s', [post_id])[0].author_id
    source = request.GET.get('from')
    state = request.GET.get('state')
    username = username_global
    cursor = connection.cursor()
    # print(f'state = {state}, {type(state)}')
    if state == '0':
        try:
            # print(f'insert into blog_like value(DEFAULT, \'{post_id}\', \'{username}\')')
            cursor.execute('insert into blog_like value(DEFAULT, %s, %s)', [post_id, username])
        except:
            request.session['self_script'] = 'alert'
            request.session['self_message'] = '点赞失败，出现了奇怪的错误'
    else:
        try:
            # print(f'delete from blog_like where blog_like.post_id_id = {post_id} and blog_like.username_id = {username}')
            cursor.execute('delete from blog_like where blog_like.post_id_id = %s and blog_like.username_id = %s', [post_id, username])
        except:
            request.session['self_script'] = 'alert'
            request.session['self_message'] = '取消点赞失败，出现了奇怪的错误'
    cursor.close()
    
    if source == 'index':
        return redirect('/blog/index/')
    elif source == 'info':
        return redirect(f'/blog/userinfo/?info={hisname}')

@identity_check
def notify(request):
    username = username_global
    # 点赞通知
    cursor = connection.cursor()
    print('select * from who_likes_me where who_likes_me.author_id = %s and who_likes_me.read = 0', [username])
    cursor.execute('select * from who_likes_me where who_likes_me.author_id = %s and who_likes_me.read = 0',[username])
    like_notify_list = list(cursor.fetchall())
    like_notify_list.sort(key=lambda x:x[0])
    like_notify_list = like_notify_list[::-1]
    cursor.close()
    print(like_notify_list)
    # 标为已读
    cursor = connection.cursor()
    cursor.execute('update who_likes_me set who_likes_me.read = 1 where who_likes_me.author_id = %s and who_likes_me.read = 0',[username])
    cursor.close()
    like_notify_list_len = len(like_notify_list)
    return render(request, 'notify.html', locals())



@identity_check
def logout(request):
    # print('===========in logout')
    global username_global
    username_global = None
    return redirect(f'/blog/login/')