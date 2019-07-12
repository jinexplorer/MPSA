from flask import Flask, render_template, request ,url_for ,redirect ,session
import pymysql

app = Flask(__name__)
db = pymysql.connect("host", "user", "password", "database")
cursor = db.cursor()

@app.route('/manager/create_team')
def create_team():
    if session.get('manager'):
        if request.method == "POST":
            team_name = request.form['team_name'] #获取社团名
            team_type = request.form['team_type'] #获取社团类别
            team_introduction = request.form['team_introduction'] #获取社团简介
            #team_logo =                                #获取社团logo
            sql = ''            #将社团信息写入数据库
            if create_team_check(team_name) == 0:  # 当不存在社团名
                    if cursor.execute(sql, [team_name,team_type,team_introduction]):  # 判断写数据库操作是否完成
                        return render_template('management.html')      #创建社团成功，返回  页面
                    else:
                        return render_template('management.html')      #创建失败，写数据库操作失败
            else:  # 当存在社团名：
                    return render_template('management.html')             #创建失败，已存在社团名称

            # 涉及写操作注意要提交
            db.commit()


        else:
            return render_template('management.html') #没有收到消息，留在原页面

    else:
        return render_template('index.html')


def create_team_check(team_name):
    if cursor.execute('SELECT * from common_user where phone_number = "%s"'%(team_name)):
        return 1
    else:
        return 0


if __name__ == '__main__':
    app.run(debug=True)