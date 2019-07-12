from flask import Flask, session,render_template, request ,redirect ,flash
import pymysql
app = Flask(__name__)
db = pymysql.connect("localhost", "jin", "liujin987", "MPSA")
cursor = db.cursor()
app.config['SECRET_KEY']='123456'


@app.route('/')
def index():
    return render_template('index.html')
'''
@app.route('/team')
def team():
    sql = "SELECT team_name,description from team"
    if cursor.execute(sql):
        team_result = cursor.fetchall()
    return render_template('index.html', team=team_result)
'''

@app.route('/login', methods=[ 'GET', 'POST' ])
def login():
    if session.get('phone_number'):
        if request.method == "POST":
            return render_template('user_login.html', error="您已登陆")
        else:
            return redirect('/user/'+session['phone_number'])
    else:
        if request.method == "POST":
            phone_number = request.form[ 'phone_number' ]
            password = request.form[ 'password' ]
            error = login_check(phone_number, password)
            if error != 1:
                return render_template('user_login.html',error=error)
            else:
                session[ 'phone_number' ] = phone_number
                return redirect('/user/'+phone_number)
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
                return 1;

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
            return redirect('/user/' + phone_number)
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
            cursor.close()
            return 1;

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
                return render_template('manage_login.html',error=error)
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
                return 1;
@app.route('/users', methods=[ 'GET', 'POST' ])
def users():
    return redirect('/user/'+session['phone_number'])

@app.route('/user/<phone_number>', methods=[ 'GET', 'POST' ])
def user(phone_number):
    if session.get('phone_number'):
        return render_template('mycommunity.html')
    else:
        return render_template('404.html')

@app.route('/mynews', methods=[ 'GET', 'POST' ])
def mynew():
    return redirect('/user/'+session['phone_number']+'/mynews')
@app.route('/user/<phone_number>/mynews', methods=[ 'GET', 'POST' ])
def mynews(phone_number):
    if session.get('phone_number'):
        return render_template('mynews.html')
    else:
        return render_template('404.html')


@app.route('/systemnew', methods=[ 'GET', 'POST' ])
def systemnew():
    return redirect('/user/'+session['phone_number']+'/systemnews')
@app.route('/user/<phone_number>/systemnews', methods=[ 'GET', 'POST' ])
def systemnews(phone_number):
    if session.get('phone_number'):
        return render_template('systemsnews.html')
    else:
        return render_template('404.html')



@app.route('/personalcenter', methods=[ 'GET', 'POST' ])
def personalcenter():
    return redirect('/user/'+session['phone_number']+'/personalcenter')
@app.route('/user/<phone_number>/personalcenter', methods=[ 'GET', 'POST' ])
def personalcenters(phone_number):
    if session.get('phone_number'):
        return render_template('pcenter.html')
    else:
        return render_template('404.html')









@app.route('/user/pcenter', methods=[ 'GET', 'POST' ])
def pcenter():
    '''
    if session.get('phone_number'):
        return render_template('pcenter.html');
    else:
        return render_template('404.html')
    '''
    if request.method == "POST":
        phone_number = request.form[ 'phone_number' ]
        password = request.form[ 'password' ]
        error = log_up_check(phone_number, password)
        if error != 1:
            return render_template('log_up.html', error=error)
        else:
            return render_template('log_up.html', sucess=1)
    else:

        return render_template('pcenter.html')




















if __name__ == '__main__':
    app.run()
