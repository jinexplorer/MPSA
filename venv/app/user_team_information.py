from flask import Flask, render_template, request ,url_for ,redirect
import pymysql

app = Flask(__name__)
db = pymysql.connect("host", "user", "password", "database")
cursor = db.cursor()

@app.route('/user_login/team_information')
def team_information():
    #社团名称
    #社团简介
    #社团创始人
    #社团公告
    sql = ''
    if cursor.execute(sql):
        team_result = cursor.fetchall()
        return render_template('  .html',result = team_result)      #获取社团信息成功，将信息返回给html并显示
    else:
        return render_template('  .html')       #获取信息失败




if __name__ == '__main__':
    app.run(debug=True)