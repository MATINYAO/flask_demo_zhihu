import random
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
from models import EmailCaptchaModel
# 引入验证码部分代码
from .froms import RegisterForm, LoginForm
from models import UserModel
# 加密密码
from werkzeug.security import generate_password_hash, check_password_hash

# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


# 也就是前面已经定义好前缀，/auth/login
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)

        # 校验部分
        if form.validate():
            # 先从前端获取变量
            email = form.email.data
            password = form.password.data

            # 在数据库中查找比对
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return render_template("login.html")

            # 验证密码
            # user.password 是从数据库中查询到的加密的密码， password是从前端输入的没有加密的密码
            if check_password_hash(user.password, password):

                # 这里引入cookie和session，cookie存储少量的数据，cookie一般用于存储登录授权的数据
                # flask中的session是加密以后存储在cookie中的。
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误！")
                return render_template("login.html")

        else:
            print(form.errors)
            return render_template("login.html")

    # 登录逻辑的实现
    # return render_template("login.html")


# GET: 从服务器上获取数据
# 这里注册，使用POST请求，将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    # 验证用户提交的邮箱和验证码是否对应且正确
    # 表单验证: flask-wtf

    if request.method == 'GET':
        # 渲染文件
        return render_template("register.html")

    # 除了get请求就是post请求
    else:
        # 验证码，密码等验证，如果通过了验证码
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            # 使用ORM模型操作数据库
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

            # 跳转到登录页面,第二种方法直接跳转，第一次方法使用url_for 视图化链接

            return redirect(url_for("auth.login"))
            # return redirect("/auth/login")

            # 通过验证的话执行注册，也就是把数据保存到数据库中

        else:
            print(form.errors)

            # 注册失败重新跳转到注册页面
            return redirect("/auth/register")




@bp.route("logout")
def logout():
    session.clear()
    return redirect("/")







# bp.route: 如果没有指定methods参数，默认就是GET请求
@bp.route("/captcha/email")
def get_email_captcha():
    # url传参数
    # /captcha/emial?email=xxx@qq.com
    email = request.args.get("email")
    print(email)
    # 6位，数字和字母的组成
    source = string.digits*6
    captcha = random.sample(source, 6)
    # 列表变成字符串
    captcha = "".join(captcha) # 965083
    print(captcha)

    # I/O 操作
    message = Message(subject="菜鸡学安全", recipients=[email], body=f"您的验证码是:{captcha}")
    mail.send(message)


    # 使用数据库存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()

    # RESTful API，这是一个格式
    # {code:200/400/500, message: "xxx", data: {}}


    return jsonify({"code":200, "message": "", "data": None})

    # memcached 和redis 适合存储验证，这里扩展，这里暂用数据库来存储



@bp.route("/mail/test")
def mail_test():
    # message = Message(subject="菜鸡学安全1111", recipients=['xxxxxx@163.com'], body="你好我是开发，你好，面试邀请，请你及时确认。")
    # mail.send(message)
    return "邮件发送成功"



