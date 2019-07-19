from flask import Flask, session, render_template, request, redirect, flash,abort
import pymysql
import hashlib
from flask import Blueprint
from werkzeug.utils import secure_filename
import os
import datetime
from flask_mail import Mail, Message
blue_manage = Blueprint('blue_manage',__name__)

app = Flask(__name__)

db = pymysql.connect("localhost", "jin", "liujin987", "MPSA")
db.autocommit(True )
cursor = db.cursor()

app.config['MAIL_SERVER'] = "smtp.qq.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "1074612393@qq.com"
app.config['MAIL_PASSWORD'] = "ejapyzfccntsfefb"

mail = Mail(app)

def md5encryption(string):
    return   hashlib.md5(string.encode('utf-8')).hexdigest()

@blue_manage.route('/manage_login', methods=[ 'GET', 'POST' ])
def manage_login():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            return render_template('manage_login.html', error="您已登陆")
        else:
            return redirect('/manager')
    else:
        if request.method == "POST":
            phone_number = request.form[ 'phone_number' ].strip()
            a=request.form[ 'password' ].strip()
            password = md5encryption(request.form[ 'password' ].strip())
            error = manage_login_check(phone_number, password)
            if error != 1:
                return render_template('manage_login.html', error=error)
            else:
                session[ 'manage_phone_number' ] = phone_number
                return redirect('/manager')
        else:
            return render_template('manage_login.html')


def manage_login_check(phone_number, password):
    if len(phone_number.strip()) == 0 or len(password.strip()) == 0:
        return "用户名或密码不能为空"
    elif len(phone_number) < 5:
        return "请输入正确的用户名"
    else:
        sql = 'SELECT * from common_user where phone_number = "%s" and password="%s"' % (phone_number, password)
        if cursor.execute(sql):
            return "账号/密码错误"
        else:
            sql = 'SELECT * from manage_user where phone_number = "%s" and password="%s"' % (phone_number, password)
            if cursor.execute(sql) == 0:
                return "账号/密码错误"
            else:
                return 1




@blue_manage.route('/contact_me', methods=[ 'GET', 'POST' ])
def contact_me():
    if request.method == "POST":
        email = request.form['email']
        reason = request.form['reason']
        message = Message(subject='管理员申请', sender='1074612393@qq.com', recipients=['hengztian@163.com'], body='from ' +email + '\n' + reason)
        mail.send(message)
        return render_template('contact_me.html',success='1')
    else:
        return render_template('contact_me.html')


@blue_manage.route('/manager_log_out', methods=[ 'GET', 'POST' ])
def manager_log_out():
    if session.get('manage_phone_number'):
        session.pop('manage_phone_number', None)
    else:
        pass
    return redirect('/');


@blue_manage.route('/manager', methods=[ 'GET', 'POST' ])
def manager():
    if session.get('manage_phone_number'):
        return redirect('/manager/mycommunity')
    else:
        return redirect('/')

@blue_manage.route('/manager/mycommunity' , methods=[ 'GET', 'POST' ])
def manager_community():
    if session.get('manage_phone_number'):
        if request.method == 'POST':
            if request.form['action'] == 'quit':
                team_name = request.form['team_name']
                sql_delete_information = 'DELETE from team where team_name = "%s"' %(team_name)
                sql_delete_user = 'DELETE from team_user where team_name = "%s"' %(team_name)
                sql_delete_message = 'DELETE from message where team_name = "%s"'% (team_name)
                cursor.execute(sql_delete_user)
                cursor.execute(sql_delete_information)
                cursor.execute(sql_delete_message)
                return redirect('/manager/mycommunity')

            else:
                get_team_name = request.form['team_name']
                sql_view = 'SELECT team_name,category,description,create_user from team where team_name = "%s"' % (
                    get_team_name)
                if cursor.execute(sql_view):
                    team_result = cursor.fetchall()
                    return render_template('manage_team_view.html', result=team_result)  # 返回到某社团信息界面
                else:
                    abort(404)
        else:
            sql_view = 'SELECT team_name,description from team where create_user = "%s"' % (session.get('manage_phone_number'))
            if cursor.execute(sql_view):
                team_result = cursor.fetchall()
                return render_template('management_mycommunity.html',result = team_result)
            else:
                return render_template('management_mycommunity.html')
    else:
        return redirect('/')
@blue_manage.route('/manager/manager_mynews', methods=[ 'GET', 'POST' ])
def manager_mynews():
    if session.get('manage_phone_number'):
        sql_myteam = 'SELECT message.team_name,title,content,create_time from team,message \
                        where create_user = "%s" and message.team_name=team.team_name ORDER BY create_time DESC' % (
        session['manage_phone_number'])
        if cursor.execute(sql_myteam):
            result = cursor.fetchall()
            result1 = manage_cut(result)
            return render_template('management_mynews.html', result=result1)
        else:
            return render_template('management_mynews.html')
    else:
        return redirect('/')

def manage_cut(a):
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

@blue_manage.route('/manager/manager_systemnews', methods=[ 'GET', 'POST' ])
def manager_systemnews():
    if session.get('manage_phone_number'):
        if request.method == 'POST':
            get_team_name = request.form['team_name']
            get_phone_number = request.form['phone_number']
            get_status = request.form['status']
            get_create_time = request.form['create_time']
            get_type = request.form['type']
            set_create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if request.form['action'] == 'accept':
                set_status = '已接受'
                sql_update = 'update systemnews set status="%s" ,create_time = "%s" where status = "%s" and phone_number="%s" and team_name = "%s" and type = "%s" and create_time = "%s" ' % ( \
                        set_status, set_create_time, get_status, get_phone_number, get_team_name, get_type, get_create_time)
                if get_type == '申请加入':
                    sql_get_name = 'SELECT name from common_user_information where phone_number = "%s" ' % (get_phone_number)
                    cursor.execute(sql_get_name)
                    user_name = cursor.fetchone()[0]

                    sql_set = 'insert into team_user(team_name,user_name,phone_number) values(%s,%s,%s); '
                    if cursor.execute(sql_set,[get_team_name,user_name,get_phone_number]):
                        if cursor.execute(sql_update):
                            flash('处理成功！')
                            return redirect('/manager/manager_systemnews')
                        else:
                            flash('未知错误')
                            return redirect('/manager/manager_systemnews')
                    else:
                        flash('未知错误，请重试')
                        return redirect('/manager/manager_systemnews')

                else:  #申请退出
                    # sql_get_name = 'SELECT name from common_user_information where phone_number = "%s" ' % (
                    #     get_phone_number)
                    # cursor.execute(sql_get_name)
                    # user_name = cursor.fetchone()[0]

                    sql_set = 'delete from team_user where team_name = "%s" and phone_number = "%s" ' % (get_team_name,get_phone_number)
                    if cursor.execute(sql_set):
                        if cursor.execute(sql_update):
                            flash('处理成功！')
                            return redirect('/manager/manager_systemnews')
                        else:
                            flash('未知错误')
                            return redirect('/manager/manager_systemnews')
                    else:
                        flash('未知错误，请重试')
                        return redirect('/manager/manager_systemnews')

            else: #当选择拒绝
                set_status = '已拒绝'
                sql_update = 'update systemnews set status="%s" ,create_time = "%s" where status = "%s" and phone_number="%s" and team_name = "%s" and type = "%s" and create_time = "%s" ' % ( \
                    set_status, set_create_time, get_status, get_phone_number, get_team_name, get_type, get_create_time)
                if cursor.execute(sql_update):
                    flash('操作成功')
                    return redirect('/manager/manager_systemnews')
                else:
                    flash('未知错误，请重试')
                    return redirect('/manager/namager_systemnews')

        else:
            sql_view = 'SELECT systemnews.team_name,type,status,create_time ,phone_number from systemnews,team where create_user = "%s" and systemnews.team_name = team.team_name and status = "%s" ORDER BY create_time DESC' % ( \
                session['manage_phone_number'],'未处理')  # 降序排序
            if cursor.execute(sql_view):
                result = cursor.fetchall()
                return render_template('management_systemsnews.html', result=result)
            else:
                return render_template('management_systemsnews.html')
    else:
        return redirect('/')

@blue_manage.route('/manager/management', methods=[ 'GET', 'POST' ])
def management():
    if session.get('manage_phone_number'):
        return render_template('management.html')
    else:
        return redirect('/')

@blue_manage.route('/manager/manager_pcenter', methods=[ 'GET', 'POST' ])
def manager_pcenter():
    if session.get('manage_phone_number'):
        return render_template('manager_pcenter.html')
    else:
        return redirect('/')

@blue_manage.route('/manager/manager_pcenter/manager_information', methods=[ 'GET', 'POST' ])
def manager_information():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            name = request.form[ 'sname' ].strip()  # 获取姓名
            student_number = request.form[ 'snumber' ].strip()  # 获取学号
            sex = request.form[ 'sex' ].strip() # 获取性别
            introduction = request.form[ 'introduction' ].strip()  # 获取个人简介
            phone_number = request.form[ 'pnumber' ].strip()
            f = request.files['file']
            if f.filename[-4:] == '.jpg':
                basepath = os.path.dirname(__file__)
                file_name = session['manage_phone_number'] + f.filename[-4:]
                upload_path = os.path.join(basepath, 'static/uploads', file_name)
                f.save(upload_path)
            else:
                flash('目前仅支持.jpg格式图片文件')

            if len(introduction) == 0:
                introduction = '这个人很懒，什么都没有留下'
            sql_change = 'update manage_user_information set name="%s",student_number = "%s" ,sex = "%s" , description ="%s" where phone_number="%s"' % (
                name, student_number, sex, introduction, phone_number)  # 修改个人信息

            if cursor.execute(sql_change):
                
                return redirect('/manager/manager_pcenter/manager_information')
            else:
                return redirect('/manager/manager_pcenter/manager_information')
        else:
            sql_view = 'select name,student_number,sex,description from manage_user_information where phone_number="%s"' % ( session[ 'manage_phone_number' ])  # 查看已有个人信息
            if cursor.execute(sql_view):  # 显示目前个人信息
                personal_result = cursor.fetchall()
                name = personal_result[ 0 ][ 0 ]
                student_number = personal_result[ 0 ][ 1 ]
                sex = personal_result[ 0 ][ 2 ]
                introduction = personal_result[ 0 ][ 3 ]
                phone_number = session[ 'manage_phone_number' ]
                filepath = '../../static/uploads/' + session['manage_phone_number'] + '.jpg'

                return render_template('manager_pcenter_information.html', name=name, student_number=student_number, \
                                       phone_number=phone_number, sex=sex, introduction=introduction ,filepath = filepath)
            else:
                return render_template('manager_pcenter_information.html', fail='个人信息修改失败,请重试')  # 如果获取数据库失败，则返回错误信息

    else:
        return redirect('/')



@blue_manage.route('/manager/manager_pcenter/manager_password', methods=[ 'GET', 'POST' ])
def manager_password():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            old_password = md5encryption(request.form[ 'oldpassword' ].strip())  # 获取原密码
            new_password = md5encryption(request.form[ 'password' ].strip() )# 获取新密码
            new_password_word = md5encryption(request.form[ 'password2' ].strip() ) # 再次输入新密码
            phone_number=session['manage_phone_number']
            if new_password == new_password_word:  # 判断两次输入密码是否相同
                if change_password_check_manage(phone_number, old_password):  # 判断原密码是否匹配
                    sql = "update manage_user set password='%s' where phone_number='%s' and password='%s'" % ( \
                        new_password, phone_number, old_password)
                    if cursor.execute(sql):  # 判断写数据库操作是否完成
                        
                        return render_template('manager_pcenter_password.html', notice='修改密码成功')

                    else:
                        return render_template('manager_pcenter_password.html', notice='未知错误')
                else:  # 当原密码与数据库中不匹配时：
                    return render_template('manager_pcenter_password.html', notice='原密码错误')
            else:  # 当两次输入密码不相同时：
                return render_template('manager_pcenter_password.html', notice='两次密码不一致！')
        # 涉及写操作注意要提交

        else:
            return render_template('manager_pcenter_password.html')  # 没有收到消息，留在原页面
    else:
        return redirect('/')


def change_password_check_manage(username, password):
    if cursor.execute('SELECT * from manage_user where phone_number = "%s" and password = "%s"' % (username, password)):
        return 1
    else:
        return 0



@blue_manage.route('/manager/management/create_team', methods=[ 'GET', 'POST' ])
def create_team():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            team_name = request.form['ogName'].strip() #获取社团名
            team_type = request.form['ogclass'].strip() #获取社团类别
            team_introduction = request.form['ogintroduction'].strip() #获取社团简介
            #team_logo =                                #获取社团logo
            sql = 'insert into team(team_name,category,description,create_user) values(%s,%s,%s,%s);'            #将社团信息写入数据库
            if create_team_check(team_name) == 0:  # 当不存在社团名
                if cursor.execute(sql, [team_name,team_type,team_introduction,session['manage_phone_number']]):  # 判断写数据库操作是否完成
                      
                      return render_template('management_create.html',notice = '创建成功')      #创建社团成功，返回原页面并提示
                else:
                      abort(404)      #创建失败，写数据库操作失败
            else:  # 当存在社团名：
                 return render_template('management_create.html',notice = '创建失败,社团已存在')             #创建失败，已存在社团名称

            # 涉及写操作注意要提交
        else:
            return render_template('management_create.html') #没有收到消息，留在原页面

    else:
        return redirect('/')


def create_team_check(team_name):
    if cursor.execute('SELECT * from team where team_name = "%s"'%(team_name)):
        return 1
    else:
        return 0




@blue_manage.route('/manager/management/people', methods=[ 'GET', 'POST' ])
def people():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            team_name=request.form['team_name'].strip()
            sql = 'select team_name from team where create_user="%s" and team_name="%s"' % (session[ 'manage_phone_number' ],team_name)
            if cursor.execute(sql):
                sql_result = cursor.fetchall()
                return render_template('management_community.html',result=sql_result)
            else:
                return render_template('management_community.html')
        else:
            sql='select team_name from team where create_user="%s"'%(session['manage_phone_number'])
            if cursor.execute(sql):
                sql_result = cursor.fetchall()
                return render_template('management_community.html',result=sql_result)
            else:
                return render_template('management_community.html')
    else:
        return redirect('/')

@blue_manage.route('/manager/management/peoples', methods=[ 'GET', 'POST' ])
def peoples():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            team_name=request.form['team_name'].strip()

            sql='select name,sex,student_number,team_user.phone_number from team_user,common_user_information where team_name="%s" and team_user.phone_number=common_user_information.phone_number'%(team_name)
            if cursor.execute(sql):
                sql_result = cursor.fetchall()
                return render_template('management_people.html', result=sql_result,team=team_name)
            else:
                return render_template('management_people.html',team=team_name)
        else:
             return render_template('management_people.html',team=team_name)
    else:
        return redirect('/')
@blue_manage.route('/delect', methods=[ 'GET', 'POST' ])
def delect():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            name = request.form[ 'name' ].strip()
            phone_number = request.form[ 'phone_number' ].strip()
            sql = 'select team_name FROM team_user where user_name="%s" and phone_number="%s"' % (name, phone_number)
            sql1='DELETE FROM team_user where user_name="%s" and phone_number="%s"'%(name,phone_number)
            if cursor.execute(sql):
                sql_result = cursor.fetchall()
                team_name=sql_result[0][0];
                if cursor.execute(sql1):
                    
                    sql2 = 'select name,sex,student_number,team_user.phone_number from team_user,common_user_information where  team_name="%s" and team_user.phone_number=common_user_information.phone_number' % (team_name.strip())
                    if cursor.execute(sql2):
                        sql_result = cursor.fetchall()
                        return render_template('management_people.html', result=sql_result,team=team_name)
                    else:
                        return render_template('management_people.html', team=team_name)
                else:
                     return render_template('management_people.html',team=team_name)
            else:
                return render_template('management_people.html')
        else:
            return render_template('management_people.html')
    else:
        return redirect('/')



@blue_manage.route('/add', methods=[ 'GET', 'POST' ])
def add():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            phone_number = request.form[ 'new_phone_number' ].strip()
            team_name = request.form[ 'team_name' ].strip()
            sql = 'select name FROM common_user_information where phone_number="%s"' % (phone_number)
            if cursor.execute(sql):
                sql_result = cursor.fetchall()
                user_name=sql_result[0][0];
                sql_sel = 'select * from  team_user where team_name="%s" and user_name="%s" and phone_number="%s"'  % ( \
                    team_name, user_name, phone_number)
                if cursor.execute(sql_sel):
                    sql2 = 'select name,sex,student_number,team_user.phone_number from team_user,common_user_information where team_name="%s" and team_user.phone_number=common_user_information.phone_number' % (
                        team_name)
                    if cursor.execute(sql2):
                        sql_result = cursor.fetchall()
                        return render_template('management_people.html', result=sql_result, team=team_name,\
                                               notice='用户已存在')
                    else:
                        return render_template('management_people.html', team=team_name, notice='用户已存在')
                else:
                    sql1 = 'insert into  team_user(team_name,user_name,phone_number) value ("%s","%s","%s")' % (\
                    team_name, user_name,phone_number)
                    if cursor.execute(sql1):
                        
                        sql2 = 'select name,sex,student_number,team_user.phone_number from team_user,common_user_information where team_name="%s" and team_user.phone_number=common_user_information.phone_number' % (
                            team_name)
                        if cursor.execute(sql2):
                            sql_result = cursor.fetchall()
                            return render_template('management_people.html', result=sql_result, team=team_name,notice='添加成功，成员信息已加入')
                        else:
                            return render_template('management_people.html', team=team_name,notice='添加成功，成员信息已加入')
                    else:
                         return render_template('management_people.html',team=team_name,notice='新增失败')
            else:
                sql2 = 'select name,sex,student_number,team_user.phone_number from team_user,common_user_information where team_name="%s" and team_user.phone_number=common_user_information.phone_number' % (
                    team_name)
                if cursor.execute(sql2):
                    sql_result = cursor.fetchall()
                    return render_template('management_people.html', result=sql_result, team=team_name, \
                                           notice='查无此人')
                else:
                    return render_template('management_people.html', team=team_name, notice='查无此人')
        else:
            return render_template('management_people.html')
    else:
        return redirect('/')


@blue_manage.route('/delete_news' , methods=[ 'GET', 'POST' ])
def delete_news():
    if session.get('manage_phone_number'):

        if request.method=='POST':
            team_name = request.form['team_name']
            title = request.form['title']
            sql = 'DELETE from message where team_name = "%s" and title = "%s"' % (team_name,title)
            if cursor.execute(sql):
                return redirect('/manager/manager_mynews')
            else:
                return redirect('/manager/manager_mynews')
        else:
            return redirect('/manager/manager_mynews')
    else:
        return redirect('/')







@blue_manage.route('/manager/management/send_message',methods=[ 'GET', 'POST' ])
def send_message(): #创建公告
    if session.get('manage_phone_number'):
        sql = 'select team_name from team where create_user="%s"' % (session[ 'manage_phone_number' ])
        if cursor.execute(sql):
            sql_result = cursor.fetchall()
            if request.method == "POST":
                sql = 'insert into message(team_name,title,content,create_time) values(%s,%s,%s,%s);'  # 将公告写入数据库(库还没写)
                team_name = request.form['team_name'].strip()  # 获取用户名
                title = request.form['headline'].strip()          #获取标题
                message = request.form['content'].strip()  # 获取公告内容
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if cursor.execute(sql,[team_name,title,message,create_time]):
                    
                    return render_template('management_publish.html',result=sql_result,notice='发布成功')  # 创建公告成功！这里应该返回的是本社团的主界面
                else:
                    return render_template('management_publish.html',notice='发生未知错误，请联系系统管理员')  # 创建公告失败，应该返回本界面

            else:
                return render_template('management_publish.html',result=sql_result)   #还未创建公告，留在本界面
        else:
            return render_template('management_publish.html',notice='请先创建一个社团')  # 还未创建公告，留在本界面

    else:
        return redirect('/') #管理员未登录


@blue_manage.route('/manage_security_question',methods=[ 'GET', 'POST' ])
def manage_security_question():
    if session.get('manage_phone_number'):
        sql_view = 'select * from security_question where phone_number="%s"' % (
            session[ 'manage_phone_number' ])  # 查看已有个人信息
        if cursor.execute(sql_view):  # 显示目前个人信息
            if request.method == "POST":
                question=request.form[ 'question' ].strip()
                password = md5encryption(request.form[ 'password' ].strip())
                answer = md5encryption(request.form['answer'].strip())
                sql_check = 'SELECT * from manage_user where phone_number = "%s" and password = "%s" ' % (session['manage_phone_number'],password)
                if cursor.execute(sql_check):
                    sql = 'update security_question set question="%s",answer="%s" where  phone_number="%s"' % (
                    question, answer, session['manage_phone_number'])
                    if cursor.execute(sql):
                        result = [[question, answer]]
                        return render_template('manage_security_question.html', result=result,
                                               notice="修改成功")  # 没有收到消息，留在原页面
                    else:
                        return render_template('manage_security_question.html', notice="未知错误修改失败")
                else:
                    return render_template('manage_security_question.html', notice="密码错误")
            else:
                result=cursor.fetchall()
                return render_template('manage_security_question.html', result=result)
        else:
            if request.method == "POST":
                question=request.form[ 'question' ].strip()
                password = md5encryption(request.form[ 'password' ].strip())
                answer = md5encryption(request.form['answer'].strip())
                sql_check = 'SELECT * from manage_user where phone_number = "%s" and password = "%s" ' % (session['manage_phone_number'],password)
                if cursor.execute(sql_check):
                    sql1 = 'insert into security_question(question,answer,phone_number) value("%s","%s","%s")'%(question,answer,session['manage_phone_number'])
                    if cursor.execute(sql1):
                        result = [ [ question, answer ] ]
                        return render_template('manage_security_question.html', result=result, notice="修改成功")  # 没有收到消息，留在原页面
                    else:
                        return render_template('manage_security_question.html', notice="未知错误修改失败")
                else:
                    return render_template('manage_security_question.html', notice="密码错误")

            else:
                return render_template('manage_security_question.html')

    else:
        return redirect('/')
