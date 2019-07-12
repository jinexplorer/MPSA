from flask import Flask, render_template, request ,url_for ,redirect
import pymysql

app = Flask(__name__)
db = pymysql.connect("host", "user", "password", "database")
cursor = db.cursor()

@app.route('/<phone_number>/add_team')
def add_team(phone_number):
    if cursor.get('username'):
        sql = 'SELECT * from team_user where phone_number = %s;'
        sql_view = 'SELECT team_name,description from team'

        if cursor.execute(sql_view):        #显示当前所有社团
            result = cursor.fetchall()
            return render_template('community.html',result = result)
        else:
            return render_template('  .html',result = 'failed')
        #当按下申请加入时，首先查询是否已经存在于这个社团中

        #按加入按钮
        if ():
            if cursor.execute(sql,[phone_number]):
                return render_template('  .html',tag = '您已提交申请或已加入')
            else:
                return render_template('  .html',tag = '申请成功')

        #按退出按钮
        elif():
            if cursor.execute(sql,[phone_number]):
                return render_template('  .html',tag = '您已申请退出')
            else:
                return render_template('  .html',tag = '您还没有加入这个社团')

    else:
        return ('login.html')


if __name__ == '__main__':
    app.run(debug=True)