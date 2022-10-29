import time
import pymongo
from flask import Flask, render_template, request,Blueprint
import random
from flask import redirect, session

# 创建蓝图对象
home_app = Blueprint('home_app',__name__)
# 设置 session 秘钥
home_app.secret_key = '123456'

# 创建数据库客户端
client = pymongo.MongoClient()
db = client.ybc




# 路由：'我的主页'
@home_app.route('/home')
def home():
    # session验证是否登录
    username = session.get('username')
    if username == None:
        # 没有登录，返回登录页面
        session['href'] = 'home'
        return redirect('/login')
    else:
        # 已登录，返回主页blog信息
        blogs = list(db.blog.find().sort('time', -1))
        return render_template('home/home.html', t_blogs=blogs)


# 创建一条 blog
@home_app.route('/create_blog', methods=['POST'])
def create_blog():
    content = request.form['content']
    mood = request.form['mood']
    username = session.get('username')
    # 生成随机头像
    heads = ['head1.png', 'head2.png', 'head3.png', 'head4.png', 'head5.png']
    head = random.choice(heads)
    # 组合发布信息并存数据库
    db.blog.insert_one({'username': username,
                        'head': head,
                        'mood': mood,
                        'content': content,
                        'time': get_date_time()})

    return redirect('/home')


# 路由：退出登录
@home_app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/welcome')


# 获取当前时间并格式化
def get_date_time():
    # 获取当前系统的时间
    now = time.localtime()
    # 转化日期格式
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', now)
    return date_time


