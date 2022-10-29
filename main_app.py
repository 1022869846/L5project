import pymongo
from flask import Flask, render_template, session, redirect, request
import time


# 【提示3】从功能模块导入蓝图对象(user_app)
from quiz_app import quiz_app
from home_app import home_app
from task_app import task_app
from user_app import user_app





# 创建Flask对象
app = Flask(__name__)
# 设置 session 秘钥
app.secret_key = '123456'



# 【提示3】把蓝图注册到web程序中(home_app、task_app、user_app)
app.register_blueprint(quiz_app)
app.register_blueprint(home_app)
app.register_blueprint(task_app)
app.register_blueprint(user_app)







# 创建数据库客户端
client = pymongo.MongoClient()
db = client.ybc


# 路由：'欢迎页面'
@app.route('/')
def welcome():
    # 获取当前系统的时间
    now = time.localtime()
    # 转化日期格式
    date_time = time.strftime('%Y-%m-%d %H:%M', now)
    return render_template('main/welcome.html',
                           t_time=date_time)

@app.route('/welcome')
def welcome1():
    # 获取当前系统的时间
    now = time.localtime()
    # 转化日期格式
    date_time = time.strftime('%Y-%m-%d %H:%M', now)
    return render_template('main/welcome.html',
                           t_time=date_time)



# 【提示4】在run功能中添加参数port=5002 
if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)
