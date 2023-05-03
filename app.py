from flask import Flask, session, g
import config
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate
from models import EmailCaptchaModel


app = Flask(__name__)
app.config.from_object(config)


# 创建app后，再与db 和app绑定
db.init_app(app)

# 初始化mail连接
mail.init_app(app)


migrate = Migrate(app, db)

# blueprint，用来做模块化的
# 蓝图，视图函数模块化，蓝图


# 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'



# before_request/before_frist_request/after_request
# hook，钩子函数，请求过程中获取想要的参数。

@app.before_request
def my_before_request():
    # from flask import session， 导入session，方便从session中获取参数
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)

        setattr(g, "user", user)
        # g 是全局变量，from flask import Flask, session, g

    else:
        # 如果不存在，就设置为Noe
        setattr(g, "user", None)



    # 上下文处理器
@app.context_processor
def my_context_processor():

    # 上下文处理器中的数据，在所有的模板之中都可以使用的。
    return {"user": g.user}
    # return {"username": "zhangsan"}







if __name__ == '__main__':
    app.run()


