from flask import Flask, render_template, request ,url_for ,redirect
import pymysql

app = Flask(__name__)
db = pymysql.connect("localhost", "root", "root", "andy")
cursor = db.cursor()


@app.route('/')
def index():
    return render_template('index.html', name="Guest")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if login_check(username, password):
            return render_template('login.html', user_name='Andy', login_status='登陆成功')
        else:
            return redirect(url_for('log_up',name = username,pwd = password))

    else:
        return render_template('login.html')


def login_check(username, password):
    if cursor.execute('SELECT * from common_user where phone_number = "%s" and password = "%s"'%(username,password)):
        return 1
    else:
        return 0

@app.route('/log_up/')
def log_up(name,pwd):
        data = [(name,pwd),]
        sql_up = "insert into common_user(phone_number,password) values(%s,%s);"
        cursor.executemany(sql_up,data)
        db.commit()
        cursor.close()
        db.close()
        return render_template('login.html',user_name = name, login_status='注册成功')

        # return 'Sign up FAILED..! Please get back and try again!...'

if __name__ == '__main__':
    app.run(debug=True)