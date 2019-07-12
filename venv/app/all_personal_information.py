from flask import Flask, render_template, request ,url_for ,redirect ,session
import pymysql

app = Flask(__name__)
db = pymysql.connect("host", "user", "password", "database")
cursor = db.cursor()

@app.route('/user_login/<phone_number>/personal_information/')
def personal_information(phone_number):
    if session.get('username'):
        if request.method == "POST":
            name = request.form['sname'] #获取姓名
            study_number = request.form['snumber'] #获取学号
            sex = request.form['gender'] #获取性别
            personal_saying = request.form['introduction']   #获取个人简介
            if len(personal_saying) == 0:
                personal_saying = 'Nothing...'
            sql_change = 'update common_user set name=%s and study_number = %s and sex = %s and personal_saying = %s where phone_number=%s;'  # 修改个人信息
            if cursor.execute(sql_change,[name,study_number,sex,personal_saying,phone_number]):  # 修改个人信息:
                return redirect(url_for('personal_information'))  # 如果数据库修改成功，则重新进入个人信息界面
            else:
                return render_template('pcenter.html', notice='个人信息修改失败,请重试')  # 如果数据库更新失败，则返回错误信息
        else:
            sql_view = ''  # 查看已有个人信息
            if cursor.execute(sql_view):  # 显示目前个人信息
                personal_result = cursor.fetchall()
                return render_template('  .html', result=personal_result)  # 将数据库结果返回给网页显示
            else:
                return render_template('  .html', tag='个人信息查找失败')  # 如果获取数据库失败，则返回错误信息

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)