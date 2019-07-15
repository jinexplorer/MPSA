from flask import Flask, session, render_template, request, redirect, flash
import pymysql
import hashlib

app = Flask(__name__)
db = pymysql.connect("localhost", "root", "root", "MPSA")
cursor = db.cursor()
app.config[ 'SECRET_KEY' ] = '123456'


def md5encryption(string):
    return   hashlib.md5(string.encode('utf-8')).hexdigest()
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/team')
def team():
    sql = "SELECT team_name,description from team"
    if cursor.execute(sql):
        team_result = cursor.fetchall()
    return render_template('team.html', team=team_result)


@app.route('/login', methods=[ 'GET', 'POST' ])
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
    if len(phone_number.strip()) == 0 or len(password.strip()) == 0:
        return "手机号或密码不能为空"
    elif len(phone_number) != 11 or int(phone_number[ 0:3 ]) not in phone_number_start:
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


@app.route('/log_up', methods=[ 'GET', 'POST' ])
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
                db.commit()
                return redirect('users')
            else:
                return render_template('404.html')
    else:
        return render_template('log_up.html')


def log_up_check(phone_number, password):
    phone_number_start = [ 130, 131, 132, 155, 156, 186, 185, 176, 134, 135, 136, 137, 138, 139, 150, 151, \
                           152, 157, 158, 159, 182, 183, 184, 188, 187, 147, 178, 133, 153, 180, 181, 189, 177 ]
    if len(phone_number) == 0 or len(password) == 0:
        return "手机或密码不能为空"
    elif len(phone_number) != 11 or int(phone_number[ 0:3 ]) not in phone_number_start:
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
            db.commit()
            return 1


@app.route('/manage_login', methods=[ 'GET', 'POST' ])
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


@app.route('/users', methods=[ 'GET', 'POST' ])
def users():
    return redirect('/user/' + session[ 'phone_number' ])


@app.route('/user/<phone_number>', methods=[ 'GET', 'POST' ])
def user(phone_number):
    if session.get('phone_number'):
        return render_template('mycommunity.html')
    else:
        return render_template('404.html')


@app.route('/mynews', methods=[ 'GET', 'POST' ])
def mynew():
    return redirect('/user/' + session[ 'phone_number' ] + '/mynews')


@app.route('/user/<phone_number>/mynews', methods=[ 'GET', 'POST' ])
def mynews(phone_number):
    if session.get('phone_number'):
        return render_template('mynews.html')
    else:
        return render_template('404.html')


@app.route('/systemnew', methods=[ 'GET', 'POST' ])
def systemnew():
    return redirect('/user/' + session[ 'phone_number' ] + '/systemnews')


@app.route('/user/<phone_number>/systemnews', methods=[ 'GET', 'POST' ])
def systemnews(phone_number):
    if session.get('phone_number'):
        return render_template('systemsnews.html')
    else:
        return render_template('404.html')


@app.route('/personalcenter', methods=[ 'GET', 'POST' ])
def personalcenter():
    return redirect('/user/' + session[ 'phone_number' ] + '/personal_center')


@app.route('/user/<phone_number>/personal_center', methods=[ 'GET', 'POST' ])
def personalcenters(phone_number):
    if session.get('phone_number'):
        return render_template('pcenter.html')
    else:
        return render_template('404.html')


@app.route('/information', methods=[ 'GET', 'POST' ])
def information():
    if request.method == "POST":
        name = request.form[ 'sname' ].strip()  # 获取姓名
        student_number = request.form[ 'snumber' ].strip()  # 获取学号
        sex = request.form[ 'sex' ].strip()  # 获取性别
        introduction = request.form[ 'introduction' ].strip()  # 获取个人简介
        phone_number = request.form[ 'pnumber' ].strip()

        if len(introduction) == 0:
            introduction = '这个人很懒，什么都没有留下'
        sql_change = 'update common_user_information set name="%s",student_number = "%s" ,sex = "%s" , description ="%s" where phone_number="%s"' % (
        name, student_number, sex, introduction, phone_number)  # 修改个人信息
        if cursor.execute(sql_change):
            db.commit()
        else:
            redirect('personalcenter')
    return redirect('/user/' + session[ 'phone_number' ] + '/informations')


@app.route('/user/<phone_number>/informations', methods=[ 'GET', 'POST' ])
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

            return render_template('pcenter_information.html', name=name, student_number=student_number, \
                                   phone_number=phone_number, sex=sex, introduction=introduction)
        else:
            return render_template('pcenter_information.html', fail='个人信息修改失败,请重试')  # 如果获取数据库失败，则返回错误信息

    else:
        return render_template('404.html')


@app.route('/passwords', methods=[ 'GET', 'POST' ])
def passwords():
    return redirect('/user/' + session[ 'phone_number' ] + '/password', code=307)


@app.route('/user/<phone_number>/password', methods=[ 'GET', 'POST' ])
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
                        db.commit()
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
        return render_template('404.html')


def change_password_check(username, password):
    if cursor.execute('SELECT * from common_user where phone_number = "%s" and password = "%s"' % (username, password)):
        return 1
    else:
        return 0


@app.route('/contact_me', methods=[ 'GET', 'POST' ])
def contact_me():
    if request.method == "POST":
        return render_template('contact_me.html',success='1')
    return render_template('contact_me.html')

@app.route('/log_out', methods=[ 'GET', 'POST' ])
def log_out():
    if session.get('phone_number'):
        session.pop('phone_number', None)
    else:
        pass
    return redirect('/');
@app.route('/manager_log_out', methods=[ 'GET', 'POST' ])
def manager_log_out():
    if session.get('manage_phone_number'):
        session.pop('manage_phone_number', None)
    else:
        pass
    return redirect('/');


@app.route('/manager', methods=[ 'GET', 'POST' ])
def manager():
    if session.get('manage_phone_number'):
        return render_template('management_mycommunity.html')
    else:
        return render_template('404.html')
@app.route('/manager/manager_mynews', methods=[ 'GET', 'POST' ])
def manager_mynews():
    if session.get('manage_phone_number'):
        return render_template('management_mynews.html')
    else:
        return render_template('404.html')
@app.route('/manager/manager_systemnews', methods=[ 'GET', 'POST' ])
def manager_systemnews():
    if session.get('manage_phone_number'):
        return render_template('management_systemsnews.html')
    else:
        return render_template('404.html')
@app.route('/manager/management', methods=[ 'GET', 'POST' ])
def management():
    if session.get('manage_phone_number'):
        return render_template('management.html')
    else:
        return render_template('404.html')

@app.route('/manager/manager_pcenter', methods=[ 'GET', 'POST' ])
def manager_pcenter():
    if session.get('manage_phone_number'):
        return render_template('manager_pcenter.html')
    else:
        return render_template('404.html')

@app.route('/manager/manager_pcenter/manager_information', methods=[ 'GET', 'POST' ])
def manager_information():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            name = request.form[ 'sname' ].strip()  # 获取姓名
            student_number = request.form[ 'snumber' ].strip()  # 获取学号
            sex = request.form[ 'sex' ].strip() # 获取性别
            introduction = request.form[ 'introduction' ].strip()  # 获取个人简介
            phone_number = request.form[ 'pnumber' ].strip()

            if len(introduction) == 0:
                introduction = '这个人很懒，什么都没有留下'
            sql_change = 'update manage_user_information set name="%s",student_number = "%s" ,sex = "%s" , description ="%s" where phone_number="%s"' % (
                name, student_number, sex, introduction, phone_number)  # 修改个人信息

            if cursor.execute(sql_change):
                db.commit()
            else:
                redirect('manager_pcenter')
        sql_view = 'select name,student_number,sex,description from manage_user_information where phone_number="%s"' % ( session[ 'manage_phone_number' ])  # 查看已有个人信息
        if cursor.execute(sql_view):  # 显示目前个人信息
            personal_result = cursor.fetchall()
            name = personal_result[ 0 ][ 0 ]
            student_number = personal_result[ 0 ][ 1 ]
            sex = personal_result[ 0 ][ 2 ]
            introduction = personal_result[ 0 ][ 3 ]
            phone_number = session[ 'manage_phone_number' ]

            return render_template('manager_pcenter_information.html', name=name, student_number=student_number, \
                                   phone_number=phone_number, sex=sex, introduction=introduction)
        else:
            return render_template('manager_pcenter_information.html', fail='个人信息修改失败,请重试')  # 如果获取数据库失败，则返回错误信息

    else:
        return render_template('404.html')



@app.route('/manager/manager_pcenter/manager_password', methods=[ 'GET', 'POST' ])
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
                        db.commit()
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
        return render_template('404.html')


def change_password_check_manage(username, password):
    if cursor.execute('SELECT * from manage_user where phone_number = "%s" and password = "%s"' % (username, password)):
        return 1
    else:
        return 0



@app.route('/manager/management/create_team', methods=[ 'GET', 'POST' ])
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
                      db.commit()
                      return render_template('management_create.html',notice = '创建成功')      #创建社团成功，返回原页面并提示
                else:
                      return render_template('404.html')      #创建失败，写数据库操作失败
            else:  # 当存在社团名：
                 return render_template('management_create.html',notice = '创建失败,社团已存在')             #创建失败，已存在社团名称

            # 涉及写操作注意要提交
        else:
            return render_template('management_create.html') #没有收到消息，留在原页面

    else:
        return render_template('404.html')


def create_team_check(team_name):
    if cursor.execute('SELECT * from team where team_name = "%s"'%(team_name)):
        return 1
    else:
        return 0




@app.route('/manager/management/people', methods=[ 'GET', 'POST' ])
def people():
    if session.get('manage_phone_number'):
        if request.method == "POST":
            team_name=request.form['team_name'].strip()
            sql = 'select team_name from team where create_user="%s" and team_name="%s"' % (session[ 'manage_phone_number' ],team_name)
        else:
            sql='select team_name from team where create_user="%s"'%(session['manage_phone_number'])
        if cursor.execute(sql):
            sql_result = cursor.fetchall()
            return render_template('management_community.html',result=sql_result)
        else:
            return render_template('management_community.html')
    else:
        return render_template('404.html')

@app.route('/manager/management/peoples', methods=[ 'GET', 'POST' ])
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
        return render_template('404.html')
@app.route('/delect', methods=[ 'GET', 'POST' ])
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
                    db.commit()
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
        return render_template('404.html')



@app.route('/add', methods=[ 'GET', 'POST' ])
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
                        db.commit()
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
        return render_template('404.html')










@app.route('/manager/management/send_message',methods=[ 'GET', 'POST' ])
def send_message(): #创建公告
    if session.get('manage_phone_number'):
        sql = 'select team_name from team where create_user="%s"' % (session[ 'manage_phone_number' ])
        if cursor.execute(sql):
            sql_result = cursor.fetchall()
            if request.method == "POST":
                sql = 'insert into message(team_name,title,content,phone_number) values(%s,%s,%s,%s);'  # 将公告写入数据库(库还没写)
                team_name = request.form['team_name'].strip()  # 获取用户名
                title = request.form['headline'].strip()          #获取标题
                message = request.form['content'].strip()  # 获取公告内容
                phone_number=session['manage_phone_number']
                if cursor.execute(sql,[team_name,title,message,phone_number]):
                    db.commit()
                    return render_template('management_publish.html',result=sql_result,notice='发布成功')  # 创建公告成功！这里应该返回的是本社团的主界面
                else:
                    return render_template('management_publish.html',notice='发生未知错误，请联系系统管理员')  # 创建公告失败，应该返回本界面

            else:
                return render_template('management_publish.html',result=sql_result)   #还未创建公告，留在本界面
        else:
            return render_template('management_publish.html',notice='请先创建一个社团')  # 还未创建公告，留在本界面

    else:
        return render_template('404.html') #管理员未登录






if __name__ == '__main__':
    app.run()