# MPSA
Management Platform for Student Associations

学生社团管理平台

后端采用python3的flask架构，数据库使用的为mysql


后端使用的语言为python3,前端使用的是html,css,javascript


文件结构：(其他文件为本地生成的文件，如要使用需要自己在本地配置，配置过程稍后有)

app-

    -template -html文件
    
    -static 
    
            -images -图片文件
            
            -css -css文件
            
            -js -javascript文件
            
            -font -字体文件
            
    -main.py -主运行文件
    
    -hashlib.py -用于md5摘要的文件
    
    ss.sql -数据库文件

ubuntu18.04 的

flask使用方法如下     https://www.jianshu.com/p/7c9ebda62214

数据库的使用方法       https://www.jianshu.com/p/4908f6e686fa

通过pip install pymysql库

将app文件放置到主文件夹夹，安装pymysql 修改数据库连接的参数，之后运行main.py文件，即可就可以在127.0.0.1:5000即可运行。
一个月的时间以内可以去http://liudjain.com 访问样式网站。欢迎大家指出BUG！



功能实现：
1.主页，社团，普通用户的登录和注册（只用手机号作为唯一的凭证），管理员的登录（注册需要联系管理员）

2.普通用户：我的社团，我的消息，系统消息，个人中心（个人信息，修改密码，返回，注销），回到主页

3.管理员：我的社团，我的消息，系统消息，社团管理（创建社团，人员管理，发布消息，返回）个人中心（个人信息，修改密码，返回，注销）

4.密码在数据库中的存放采用hashlib文件中的md5算法。由于hashlib库用pip总是安装失败.所以我直接去github上copy源文件了。

5.访问登录控制采用session控制，登录成功的时候创建一个session,当浏览器关闭的时候session丢失。
