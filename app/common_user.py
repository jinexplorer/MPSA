from flask import Flask, session, render_template, request, redirect, flash,abort
from flask import Blueprint
import pymysql
import hashlib
from werkzeug.utils import secure_filename
import os
import datetime

blue_common = Blueprint('blue_common',__name__)


db = pymysql.connect("localhost", "jin", "liujin987", "MPSA")
db.autocommit(True )
cursor = db.cursor()

def md5encryption(string):
    return   hashlib.md5(string.encode('utf-8')).hexdigest()

@blue_common.route('/login', methods=[ 'GET', 'POST' ])
def login():
    if session.get('phone_number'):
        if request.method == "POST":
            return render_template('user_login.html', error="您已登陆")
        else:
            return redirect('/user/' + session[ 'phone_number' ])
    else:
        if request.method == "POST":
            phone_number = request.form[ 'phone_number' ].strip()
            password = md5encryption(request.form[ 'password' ].strip())
            error = login_check(phone_number, password)
            if error != 1:
                return render_template('user_login.html', error=error)
            else:
                session[ 'phone_number' ] = phone_number
                return redirect('/user/' + phone_number)
        else:
            return render_template('user_login.html')


def login_check(phone_number, password):
    phone_number_start = [ 130, 131, 132, 155, 156, 186, 185, 176, 134, 135, 136, 137, 138, 139, 150, 151, \
                           152, 157, 158, 159, 182, 183, 184, 188, 187, 147, 178, 133, 153, 180, 181, 189, 177 ]
    if len(phone_number) != 11 or int(phone_number[ 0:3 ]) not in phone_number_start:
        return "请输入正确的手机号"
    else:
        sql = 'SELECT * from manage_user where phone_number = "%s" and password="%s"' % (phone_number, password)
        if cursor.execute(sql):
            return "手机号/密码错误"
        else:
            sql = 'SELECT * from common_user where phone_number = "%s" and password="%s"' % (phone_number, password)
            if cursor.execute(sql) == 0:
                return "手机号/密码错误"
            else:
                return 1

@blue_common.route('/log_up', methods=[ 'GET', 'POST' ])
def log_up():
    if request.method == "POST":
        phone_number = request.form[ 'phone_number' ].strip()
        password = md5encryption(request.form[ 'password' ].strip())
        error = log_up_check(phone_number, password)
        if error != 1:
            return render_template('log_up.html', error=error)
        else:
            session[ 'phone_number' ] = phone_number
            sql = 'insert into common_user_information(phone_number,student_number,sex,name,description) values(%s,%s,%s,%s,%s);'
            if cursor.execute(sql, [ phone_number, '20xxxxxxxxxxx', '男', '未命名', '这个人很懒，什么也没有留下' ]):
                
                return redirect('users')
            else:
                abort(404)
    else:
        return render_template('log_up.html')


def log_up_check(phone_number, password):
    phone_number_start = [ 130, 131, 132, 155, 156, 186, 185, 176, 134, 135, 136, 137, 138, 139, 150, 151, \
                           152, 157, 158, 159, 182, 183, 184, 188, 187, 147, 178, 133, 153, 180, 181, 189, 177 ]
    if len(phone_number) != 11 or int(phone_number[ 0:3 ]) not in phone_number_start:
        return "请输入正确的手机号"
    else:
        sql = 'SELECT * from manage_user where phone_number = "%s"' % (phone_number)
        sql2 = 'SELECT * from common_user where phone_number = "%s"' % (phone_number)
        if cursor.execute(sql) or cursor.execute(sql2):
            return "手机号已注册"
        else:
            data = [ (phone_number, password), ]
            sql_up = "insert into common_user(phone_number,password) values(%s,%s);"
            cursor.executemany(sql_up, data)
            
            return 1

@blue_common.route('/users', methods=[ 'GET', 'POST' ])
def users():
    return redirect('/user/' + session[ 'phone_number' ])


@blue_common.route('/user/<phone_number>', methods=[ 'GET', 'POST' ])
def user(phone_number):
    if session.get('phone_number'):
        return redirect('/mycommunity')
    else:
        return redirect('/')


@blue_common.route('/mynews', methods=[ 'GET', 'POST' ])
def mynew():
    return redirect('/user/' + session[ 'phone_number' ] + '/mynews')


@blue_common.route('/user/<phone_number>/mynews', methods=[ 'GET', 'POST' ])
def mynews(phone_number):
    if session.get('phone_number'):
        sql_myteam = 'SELECT message.team_name,title,content,create_time from team_user,message \
                        where team_user.phone_number = "%s" and message.team_name=team_user.team_name ORDER BY create_time DESC' % (session['phone_number'])
        if cursor.execute(sql_myteam):
            result = cursor.fetchall()
            result1 = cut(result)
            return render_template('mynews.html',result = result1)
        else:
            return render_template('mynews.html')
    else:
        return redirect('/')

def cut(a):
    a=list(a)
    b=[ ]
    for i in a:
        i=list(i)
        if len(i[2])>40:
            i.append(i[2][40:])
            i[2]=i[2][:40]
        else:
            i.append("")
        b.append(i)
    return b

@blue_common.route('/systemnew')
def systemnew():
    return redirect('/user/' + session[ 'phone_number' ] + '/systemnews')


@blue_common.route('/user/<phone_number>/systemnews')
def systemnews(phone_number):
    if session.get('phone_number'):
        sql_view = 'SELECT team_name,type,status,create_time from systemnews where phone_number = "%s" ORDER BY create_time DESC' % (phone_number)  #降序排序
        if cursor.execute(sql_view):
            result = cursor.fetchall()
            return render_template('systemsnews.html',result = result)
        else:
            return render_template('systemsnews.html')

    else:
        return redirect('/')


@blue_common.route('/personalcenter', methods=[ 'GET', 'POST' ])
def personalcenter():
    return redirect('/user/' + session[ 'phone_number' ] + '/personal_center')


@blue_common.route('/user/<phone_number>/personal_center', methods=[ 'GET', 'POST' ])
def personalcenters(phone_number):
    if session.get('phone_number'):
        return render_template('pcenter.html')
    else:
        return redirect('/')

@blue_common.route('/information', methods=[ 'GET', 'POST' ])
def information():
    if request.method == "POST":
        name = request.form[ 'sname' ].strip()  # 获取姓名
        student_number = request.form[ 'snumber' ].strip()  # 获取学号
        sex = request.form[ 'sex' ].strip()  # 获取性别
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        if f.filename[-4:] == '.jpg':
            file_name = session['phone_number'] + '.jpg'
            upload_path = os.path.join(basepath, 'static/uploads', file_name)
            f.save(upload_path)
        else:
            flash('目前仅支持.jpg格式图片文件')
        introduction = request.form[ 'introduction' ].strip()  # 获取个人简介
        phone_number = request.form[ 'pnumber' ].strip()

        if len(introduction) == 0:
            introduction = '这个人很懒，什么都没有留下'
        sql_change = 'update common_user_information set name="%s",student_number = "%s" ,sex = "%s" , description ="%s" where phone_number="%s"' % (
        name, student_number, sex, introduction, phone_number)  # 修改个人信息
        if cursor.execute(sql_change):
            
            return redirect('/user/' + session[ 'phone_number' ] + '/informations')
        else:
            return redirect('/user/' + session[ 'phone_number' ] + '/informations')
    else:
        return redirect('/user/' + session[ 'phone_number' ] + '/informations')


@blue_common.route('/user/<phone_number>/informations', methods=[ 'GET', 'POST' ])
def informations(phone_number):
    if session.get('phone_number'):
        sql_view = 'select name,student_number,sex,description from common_user_information where phone_number="%s"' % (
            session[ 'phone_number' ])  # 查看已有个人信息
        if cursor.execute(sql_view):  # 显示目前个人信息
            personal_result = cursor.fetchall()
            name = personal_result[ 0 ][ 0 ]
            student_number = personal_result[ 0 ][ 1 ]
            sex = personal_result[ 0 ][ 2 ]
            introduction = personal_result[ 0 ][ 3 ]
            phone_number = session[ 'phone_number' ]
            filepath = '../../static/uploads/' + session['phone_number'] + '.jpg'
            return render_template('pcenter_information.html', name=name, student_number=student_number, \
                                   phone_number=phone_number, sex=sex, introduction=introduction ,filepath = filepath)
        else:
            return render_template('pcenter_information.html', fail='个人信息查看失败,请重试')  # 如果获取数据库失败，则返回错误信息

    else:
        return redirect('/')

@blue_common.route('/passwords', methods=[ 'GET', 'POST' ])
def passwords():
    return redirect('/user/' + session[ 'phone_number' ] + '/password', code=307)


@blue_common.route('/user/<phone_number>/password', methods=[ 'GET', 'POST' ])
def password(phone_number):
    if session.get('phone_number'):
        if request.method == "POST":
            old_password = md5encryption(request.form[ 'oldpassword' ].strip())  # 获取原密码
            new_password = md5encryption(request.form[ 'password' ].strip() )# 获取新密码
            new_password_word = md5encryption(request.form[ 'password2' ].strip() ) # 再次输入新密码
            if new_password == new_password_word:  # 判断两次输入密码是否相同
                if change_password_check(phone_number, old_password):  # 判断原密码是否匹配
                    sql = "update common_user set password='%s' where phone_number='%s' and password='%s'" % ( \
                        new_password, phone_number, old_password)
                    if cursor.execute(sql):  # 判断写数据库操作是否完成
                        
                        return render_template('pcenter_password.html', notice='修改密码成功')

                    else:
                        return render_template('pcenter_password.html', notice='未知错误')
                else:  # 当原密码与数据库中不匹配时：
                    return render_template('pcenter_password.html', notice='原密码错误')
            else:  # 当两次输入密码不相同时：
                return render_template('pcenter_password.html', notice='两次密码不一致！')
        # 涉及写操作注意要提交

        else:
            return render_template('pcenter_password.html')  # 没有收到消息，留在原页面
    else:
        return redirect('/')

def change_password_check(username, password):
    if cursor.execute('SELECT * from common_user where phone_number = "%s" and password = "%s"' % (username, password)):
        return 1
    else:
        return 0

@blue_common.route('/log_out', methods=[ 'GET', 'POST' ])
def log_out():
    if session.get('phone_number'):
        session.pop('phone_number', None)
    else:
        pass
    return redirect('/');

@blue_common.route('/common_apply_in')
def apply_in():
    if session.get('phone_number'):
        if request.method == 'POST':
            phone_number = session['phone_number']
            team_name = request.form['team_name']
            type = 'applyin'
            status = 'waiting'
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql_apply_check = 'SELECT * from team_user where phone_number = "%s" and team_name = "%s"' % (phone_number,team_name)
            if cursor.execute(sql_apply_check):  #已经加入了这个社团
                return render_template('.html',notice = '您已加入该社团')
            else:
                sql_apply_in = 'insert into systemnews(phone_number,team_name,type,status,create_time) values(%s,%s,%s,%s,%s);'
                if cursor.execute(sql_apply_in,[phone_number,team_name,type,status,create_time]):
                    # flash('申请成功，请耐心等待管理员审批')
                    return render_template('.html',notice = '申请成功，请耐心等待管理员审批')
                else:
                    return render_template('.html',notice = '操作失败，您是不是已经申请该社团了呢？')    #操作数据库失败，留在原界面
        else:
            return render_template('.html')  #没有收到消息，留在原界面
    else:
        return redirect('/')
@blue_common.route('/security_question',methods=[ 'GET', 'POST' ])
def security_question():
    if session.get('phone_number'):
        sql_view = 'select * from security_question where phone_number="%s"' % (
            session[ 'phone_number' ])  # 查看已有个人信息
        if cursor.execute(sql_view):  # 显示目前个人信息
            if request.method == "POST":
                question=request.form[ 'question' ].strip()
                password = md5encryption(request.form['password'].strip())
                answer = md5encryption(request.form[ 'answer' ].strip())
                sql_check = 'SELECT * from common_user where phone_number = "%s" and password = "%s" ' % (
                session['phone_number'], password)
                if cursor.execute(sql_check):
                    sql='update security_question set question="%s",answer="%s" where  phone_number="%s"'%(question,answer,session['phone_number'])
                    if cursor.execute(sql):
                        result=[[question,answer]]
                        return render_template('security_question.html',result=result,notice="修改成功")  # 没有收到消息，留在原页面
                    else:
                        return render_template('security_question.html',notice="未知错误修改失败")
                else:
                    return render_template('security_question.html',notice = "密码错误!")
            else:
                result=cursor.fetchall()
                return render_template('security_question.html', result=result)
        else:
            if request.method == "POST":
                question = request.form[ 'question' ].strip()
                password = md5encryption(request.form['password'].strip())
                answer = md5encryption(request.form[ 'answer' ].strip())
                sql_check = 'SELECT * from common_user where phone_number = "%s" and password = "%s" ' % (
                session['phone_number'], password)
                if cursor.execute(sql_check):

                    sql1 = 'insert into security_question(question,answer,phone_number) value("%s","%s","%s")'%(question,answer,session['phone_number'])
                    if cursor.execute(sql1):
                        result = [ [ question, answer ] ]
                        return render_template('security_question.html', result=result, notice="修改成功")  # 没有收到消息，留在原页面
                    else:
                        return render_template('security_question.html', notice="未知错误修改失败")
                else:
                    return render_template('security_question.html',notice = "密码错误!")

            else:
                return render_template('security_question.html')

    else:
        return redirect('/')
