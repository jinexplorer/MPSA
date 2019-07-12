from flask import Flask, render_template, request ,url_for ,redirect ,session
import pymysql

app = Flask(__name__)
db = pymysql.connect("host", "user", "password", "database")
cursor = db.cursor()

app.route('/manager/send_message')
def send_message(): #创建公告
    if session.get('manager'):
        if request.method == "POST":
            sql = ''  # 将公告写入数据库
            team_name = request.form['team_name']  # 获取用户名
            title = request.form['title']          #获取标题
            messsage = request.form['message']  # 获取公告内容
            if cursor.execute(sql):
                return render_template('  .html')  # 创建公告成功！这里应该返回的是本社团的主界面
            else:
                return render_template('  .html')  # 创建公告失败，应该返回本界面

        else:
            return render_template('  .html')   #还未创建公告，留在本界面

    else:
        return render_template('index.html') #管理员未登录




if __name__ == '__main__':
    app.run(debug=True)