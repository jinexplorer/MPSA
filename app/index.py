from flask import Flask, session, render_template, request, redirect, flash,abort
import pymysql
import hashlib
from flask_wtf.csrf import CSRFProtect,CSRFError
from flask import Blueprint
from geetest import GeetestLib
import jieba
pc_geetest_id = "48a6ebac4ebc6642d68c217fca33eb4d"
pc_geetest_key = "4f1c085290bec5afdc54df73535fc361"
mobile_geetest_id = "48a6ebac4ebc6642d68c217fca33eb4d"
mobile_geetest_key = "4f1c085290bec5afdc54df73535fc361"

db = pymysql.connect("localhost", "jin", "liujin987", "MPSA")
db.autocommit(True )
cursor = db.cursor()

blue_index = Blueprint('blue_index',__name__)

def md5encryption(string):
    return   hashlib.md5(string.encode('utf-8')).hexdigest()

@blue_index.route('/')
def index():
    if session.get('phone_number'):
        return render_template('index.html', common_login='1')  # 已登录的时候的index界面
    elif session.get('manage_phone_number'):
        return render_template('index.html', manage_login='1')
    else:
        return render_template('index.html', no_login='1')


@blue_index.route('/team')
def team():
    sql = "SELECT team_name,description from team"
    if cursor.execute(sql):
        team_result = (cursor.fetchall())
        if session.get('phone_number'):
            return render_template('team.html', common_login='1', team=team_result)
        elif session.get('manage_phone_number'):
            return render_template('team.html', manage_login='1', team=team_result)
        else:
            return render_template('team.html', no_login='1', team=team_result)
    else:
        return render_template('team.html')

@blue_index.route('/forget_password', methods=[ 'GET', 'POST' ])
def forget_password():
    if request.method == "POST":
        phone_number = request.form[ 'phone_number' ].strip()
        question = request.form[ 'question' ].strip()
        answer = md5encryption(request.form[ 'answer' ].strip())
        password = request.form[ 'password' ].strip()
        sql1 = 'select question,answer from security_question where phone_number="%s"' % (phone_number)
        if cursor.execute(sql1):
            security_question = cursor.fetchall()
            if question:
                if question == security_question[ 0 ][ 0 ] and answer == security_question[ 0 ][ 1 ]:
                    if password:
                        password = md5encryption(password)
                        sql2 = 'update common_user set password="%s" where phone_number="%s"' % (password, phone_number)
                        sql3 = 'update manage_user set password="%s" where phone_number="%s"' % (password, phone_number)
                        if cursor.execute(sql2) or cursor.execute(sql3):
                            return render_template('forget_password.html', error='密码修改成功')
                        else:
                            return render_template('forget_password.html', error='密码修改失败')
                    else:
                        return render_template('forget_password.html', phone_number=phone_number,
                                               error="密保问题正确，请填写修改后的密码",security_question=security_question[ 0 ][ 0 ])
                else:
                    return render_template('forget_password.html', phone_number=phone_number, error="密保问题答案错误",
                                           security_question=security_question[ 0 ][ 0 ])
            else:
                return render_template('forget_password.html', security_question=security_question[ 0 ][ 0 ],
                                       phone_number=phone_number)
        else:
            return render_template('forget_password.html', error="用户密保问题不存在")

    else:
        return render_template('forget_password.html')



@blue_index.route('/search', methods=['GET','POST'])
def search():
    if session.get('phone_number'):
        if request.method == 'POST':
            search_result = []
            # 取出待搜索keyword
            keyword = request.form['keyword']
            # 对keyword分词
            cut_keywords = jieba.cut_for_search(keyword)
            # 遍历所有切分出来的词，搜索数据库，这里不想做去重了
            for cut_keyword in cut_keywords:
                search_result.extend(sql_query(cut_keyword))
            # 记录搜到了多少数据
            search_result = set(search_result)
            search_nums = len(search_result)
            return render_template('search_result.html', search_result=search_result, search_nums=search_nums, \
                                   keyword=keyword)
        else:
            return render_template('search.html')
    elif session.get('manage_phone_number'):
        if request.method == 'POST':
            search_result = []
            # 取出待搜索keyword
            keyword = request.form['keyword']
            # 对keyword分词
            cut_keywords = jieba.cut_for_search(keyword)
            # 遍历所有切分出来的词，搜索数据库，这里不想做去重了
            for cut_keyword in cut_keywords:
                search_result.extend(sql_query(cut_keyword))
            # 记录搜到了多少数据
            search_result = set(search_result)
            search_nums = len(search_result)
            return render_template('manage_search_result.html', search_result=search_result, search_nums=search_nums, \
                                   keyword=keyword)
        else:
            return render_template('manage_search.html')


    else:
        return redirect('/login')

def sql_query(keyword):
    sql= "select team_name, category, description, create_user from team where team_name like '%{keyword}%' or category like '%{keyword}%' or description like '%{keyword}%'".format(keyword=keyword)
    if cursor.execute(sql):
        result=cursor.fetchall()
        return result
    else:
        return ""

@blue_index.errorhandler(CSRFError)
def handle_csrf_error(e):
    abort(404)


#极验验证码需要
@blue_index.route('/pc-geetest/register', methods=["GET"])
def get_pc_captcha():
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    session[gt.GT_STATUS_SESSION_KEY] = status
    session["user_id"] = user_id
    response_str = gt.get_response_str()
    return response_str

@blue_index.route('/mobile-geetest/register', methods=["GET"])
def get_mobile_captcha():
    user_id = 'test'
    gt = GeetestLib(mobile_geetest_id, mobile_geetest_key)
    status = gt.pre_process(user_id)
    session[gt.GT_STATUS_SESSION_KEY] = status
    session["user_id"] = user_id
    response_str = gt.get_response_str()
    return response_str
#