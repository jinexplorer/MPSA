from flask import Flask, session, render_template, request, redirect, flash
import pymysql

app = Flask(__name__)
db = pymysql.connect("localhost", "jin", "liujin987", "MPSA")
cursor = db.cursor()
app.config[ 'SECRET_KEY' ] = '123456'


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
            phone_number = request.form[ 'phone_number' ]
            password = request.form[ 'password' ]
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
        phone_number = request.form[ 'phone_number' ]
        password = request.form[ 'password' ]
        error = log_up_check(phone_number, password)
        if error != 1:
            return render_template('log_up.html', error=error)
        else:
            session[ 'phone_number' ] = phone_number
            return redirect('users')
    else:
        return render_template('log_up.html')


def log_up_check(phone_number, password):
    phone_number_start = [ 130, 131, 132, 155, 156, 186, 185, 176, 134, 135, 136, 137, 138, 139, 150, 151, \
                           152, 157, 158, 159, 182, 183, 184, 188, 187, 147, 178, 133, 153, 180, 181, 189, 177 ]
    if len(phone_number.strip()) == 0 or len(password.strip()) == 0:
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
            phone_number = request.form[ 'phone_number' ]
            password = request.form[ 'password' ]
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
        name = request.form[ 'sname' ]  # 获取姓名
        student_number = request.form[ 'snumber' ]  # 获取学号
        sex = request.form[ 'sex' ]  # 获取性别
        introduction = request.form[ 'introduction' ].strip()  # 获取个人简介
        phone_number = request.form[ 'pnumber' ]

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
            old_password = request.form[ 'oldpassword' ]  # 获取原密码
            new_password = request.form[ 'password' ]  # 获取新密码
            new_password_word = request.form[ 'password2' ]  # 再次输入新密码
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


@app.route('/log_out', methods=[ 'GET', 'POST' ])
def log_out():
    if session[ 'phone_number' ]:
        session.pop('phone_number', None)
    else:
        pass
    return redirect('/');




if __name__ == '__main__':
    app.run()
