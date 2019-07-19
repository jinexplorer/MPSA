from flask import Flask, session, render_template, request, redirect, flash,abort
from flask import Blueprint
import pymysql
import hashlib
import datetime

db = pymysql.connect("localhost", "jin", "liujin987", "MPSA")
db.autocommit(True)
cursor = db.cursor()

blue_team_information = Blueprint('blue_team_information',__name__)


@blue_team_information.route('/mycommunity' ,methods = ['GET','POST'])
def mycommunity():
    if request.method == 'POST':
        return redirect('/user/' + session['phone_number'] + '/mycommunities', code=307)
    else:
        return redirect('/user/' + session['phone_number'] + '/mycommunities')
@blue_team_information.route('/user/<phone_number>/mycommunities', methods = ['GET','POST'])
def mycommunities(phone_number):
    if session.get('phone_number'):
        if request.method == 'POST':
            if request.form['action'] == 'quit':
                phone_number = session['phone_number']
                team_name = request.form['team_name']
                type = '申请退出'
                status = '未处理'
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql_apply_check = 'SELECT * from team_user where phone_number = "%s" and team_name = "%s"' % ( \
                                                                                                phone_number, team_name)
                if cursor.execute(sql_apply_check):  # 已经加入了这个社团
                    sql_apply_in = 'insert into systemnews(phone_number,team_name,type,status,create_time) values(%s,%s,%s,%s,%s);'
                    sql_apply_in_check = 'select * from systemnews where phone_number = "%s" and team_name = "%s" and type = "%s" and status = "%s" ' % (\
                                                                                                        phone_number,team_name,type,'未处理')
                    if cursor.execute(sql_apply_in_check):
                        flash('操作失败，您是不是已经申请该社团了呢？')
                        return redirect('/mycommunity')  # 操作数据库失败，留在原界面
                    else:
                        if cursor.execute(sql_apply_in, [phone_number, team_name, type, status, create_time]):
                            flash('申请成功，请耐心等待管理员审批')
                            return redirect('/mycommunity')
                        else:
                            flash('操作失败，您是不是已经申请该社团了呢？')
                            return redirect('/mycommunity')  # 操作数据库失败，留在原界面
                else:
                    return render_template('404.html', notice='您未加入该社团')
            else:
                get_phone_number = request.form['phone_number']
                get_team_name = request.form['team_name']
                sql_view = 'SELECT team_name,category,description,create_user from team where team_name = "%s"' %(get_team_name)
                if cursor.execute(sql_view):
                    team_result = cursor.fetchall()
                    return render_template('team_view.html',result = team_result)        #返回到某社团信息界面
                else:
                    abort(404)
        else:   #显示当前我加入的社团
            sql = 'SELECT team_name,user_name,phone_number from team_user where phone_number = "%s"' % (phone_number)
            # sql2 = 'SELECT description from team where team_name = "%s"' % (get_team_name)
            if cursor.execute(sql):
                mycommunity = cursor.fetchall()

                return render_template('mycommunity.html', result=mycommunity)
            else:
                return render_template('mycommunity.html')
    else:
        return redirect('/')

@blue_team_information.route('/applyin_community',methods = ['POST','GET'])
def apply_in():
    if session.get('phone_number'):
        if request.method == 'POST':
            team_name = request.form['team_name']
            phone_number = session['phone_number']
            type = '申请加入'
            status = '未处理'
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = 'insert into systemnews(phone_number,team_name,type,status,create_time) values(%s,%s,%s,%s,%s);'
            sql_check = 'SELECT * from team_user where phone_number = "%s" and team_name = "%s"' %(phone_number,team_name)
            if cursor.execute(sql_check):
                flash('您已加入该社团')
                return redirect('/team')
            else:
                sql_apply_check = 'select * from systemnews where team_name = "%s" and phone_number = "%s" and  type = "%s" and status = "%s" '
                if cursor.execute(sql_apply_check,[team_name,phone_number,type,status]):
                    flash('请勿重复申请')
                    return redirect('/team')
                else:

                    if cursor.execute(sql, [ phone_number, team_name, type, status, create_time ]):
                        flash('申请加入成功，请耐心等待管理员审批！')
                        return redirect('/team')
                    else:
                        flash('申请失败，请重试')
                        return redirect('/team')


        else:
            return redirect('/team')
    elif session.get('manage_phone_number'):
        flash('管理员不可以加入社团，请用普通用户重试')
        return redirect('/team')
    else:
        return redirect('/')