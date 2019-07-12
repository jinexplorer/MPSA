from flask import Flask, render_template, request ,url_for ,redirect ,session ,flash
import pymysql

app = Flask(__name__)
db = pymysql.connect("host", "user", "password", "database")
cursor = db.cursor()

@app.route('/user_login/<phone_number>/change_password/')
#修改密码模块
def change_password(phone_number):      #应传入当前已登录的用户名（phone_number)
    if session.get('username'):
        sql = "update common_user set password=%s where phone_number=%s;"
        if request.method == "POST":
            password = request.form['oldpassword'] #获取原密码
            new_password = request.form['password'] #获取新密码
            new_password_word = request.form['password2']   #再次输入新密码
            if new_password == new_password_word:  # 判断两次输入密码是否相同
                if change_password_check(phone_number, password):  # 判断原密码是否匹配
                    if cursor.execute(sql, [new_password,phone_number] ):  # 判断写数据库操作是否完成
                        return render_template('pcenter.html',notice = '修改密码成功')
                    else:
                        return 'Unknown WRONG...'
                else:  # 当原密码与数据库中不匹配时：
                    return render_template('pcenter.html',notice = '原密码错误')
            else:  # 当两次输入密码不相同时：
                return render_template('pcenter.html',notice = '两次密码不一致！')
        # 涉及写操作注意要提交
            db.commit()

        else:
            return render_template('pcenter.html') #没有收到消息，留在原页面
    else:
        return render_template('index.html',notice = '账号登录过期，请重新登录!')


#检测原密码
def change_password_check(username,password):
    if cursor.execute('SELECT * from common_user where phone_number = "%s" and password = "%s"'%(username,password)):
        return 1
    else:
        return 0

if __name__ == '__main__':
    app.run(debug=True)