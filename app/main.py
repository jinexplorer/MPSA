from flask import Flask, session, render_template, request, redirect, flash, make_response, send_from_directory, abort
from index import blue_index
from manager_user import blue_manage
from common_user import blue_common
from team_information import blue_team_information
import pymysql
import hashlib
from werkzeug import secure_filename
from flask_mail import Mail, Message
import jieba
from flask_wtf.csrf import CSRFProtect,CSRFError
from datetime import timedelta

#CRSF保护开启
csrf = CSRFProtect()
app = Flask(__name__)
csrf.init_app(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)


#数据库
db = pymysql.connect("localhost", "jin", "liujin987", "MPSA")
db.autocommit(True )
cursor = db.cursor()
#蓝图注册
app.register_blueprint(blue_index)
app.register_blueprint(blue_manage)
app.register_blueprint(blue_common)
app.register_blueprint(blue_team_information)

#邮箱配置
app.config['MAIL_SERVER'] = "smtp.qq.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "1074612393@qq.com"
app.config['MAIL_PASSWORD'] = "ejapyzfccntsfefb"
mail = Mail(app)

#run
if __name__ == '__main__':
    app.secret_key = 'i-like-python-nmba'
    app.run(host='0.0.0.0')
