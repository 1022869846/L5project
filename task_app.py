import pymongo
from flask import Flask, render_template, session, redirect, request, Blueprint
import time, uuid

# 创建蓝图对象
task_app = Blueprint('task_app', __name__)
# 设置 session 秘钥
task_app.secret_key = '123456'

# 创建数据库客户端
client = pymongo.MongoClient()
db = client.ybc


# 获取当前时间并格式化
def get_date_time():
    # 获取当前系统的时间
    now = time.localtime()
    # 转化日期格式
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', now)
    return date_time


'''
    --------与任务本有关的路由--------

    /task             访问“任务列表页面”，实现查询任务功能
    /add_task         访问“新建任务页面”
    /add_check        处理新建任务表单，实现添加任务功能
    /update_task      修改任务状态
    /delete_task      将任务状态修改为“删除”
'''


# 路由：返回“任务列表页面”
@task_app.route('/task')
def task():
    # 没有登录，不能访问
    username = session.get('username')

    if username == None:
        # 保存当前即将跳转的页面
        session['href'] = 'task'
        return redirect('/login')
    else:
        # 获取提交的科目（subject）
        subject = request.args.get('subject')
        if subject is None or subject == '全部':
            tasks = list(db.task.find({'username': username}))
        else:
            tasks = list(db.task.find({'username': username, 'subject': subject}))

        # 使用todo_find()函数查询符合条件的任务数据
        options = ['全部', '语文', '数学', '英语', '编程']

        # 返回任务页面
        return render_template('task/task.html',
                               t_username=username,
                               t_tasks=tasks,
                               t_options=options,
                               t_subject=subject)


# 路由：返回“新建任务页面”
@task_app.route('/add_task')
def add_task():
    # 没有登录，不能访问
    username = session.get('username')
    if username == None:
        return redirect('/login')
    # 已登录
    else:
        # 可选科目
        options = ['语文', '数学', '英语', '编程']
        return render_template('task/add_task.html',
                               t_options=options)


# 路由：实现新建任务功能
@task_app.route('/add_check', methods=['POST'])
def add_check():
    # 组装一条任务数据 task
    username = session.get('username')
    data = {
        'subject': request.form.get('subject'),
        'content': request.form.get('content'),
        '_id': str(uuid.uuid1()),
        'state': '未完成',
        'username': username,
        'time': get_date_time()
    }

    # 将新任务增加到数据库中
    db.task.insert_one(data)

    # 重定向到任务本主页
    return redirect('/task')


# 路由：实现将任务状态
@task_app.route('/update_task')
def update_task():
    # 如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')
    else:
        # 获取超链接提交的数据（_id），赋值给变量_id
        _id = request.args.get('_id')
        state = request.args.get('state')
        res = db.task.find_one({"_id": _id})
        if res is not None:
            if state == '未完成':
                res['state'] = '已完成'
            elif state == '已完成':
                res['state'] = '未完成'
            db.task.update({'_id': _id}, res)

        # 重定向到任务列表页面
        return redirect('/task')


# 路由：实现将任务设置为“删除”
@task_app.route('/delete_task')
def delete_task():
    # 如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')
    else:
        # 获取链接提交的数据（_id），赋值给变量_id
        _id = request.args.get('_id')
        res = db.task.find_one({'_id': _id})

        if res:
            res['state'] = '已删除'
            db.task.update({'_id': _id}, res)

        # 重定向到任务列表页面
        return redirect('/task')
