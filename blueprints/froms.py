import wtforms
from wtforms.validators import Email, Length, EqualTo
# 导入数据库模型
from models import UserModel, EmailCaptchaModel
from exts import db

# 后端校验,验证器

# 继承自wtfforms中的表单功能直接使用
class RegisterForm(wtforms.Form):
    # 验证器validators
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误，请重新输入！")])
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message='验证码格式错误！')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误，3-20位。")])
    password = wtforms.StringField(validators=[Length(min=8, max=20, message="密码格式错误，8-20位")])
    # 再次确认密码是否一致
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致，请重新输入！")])



    # 自定义验证
    # 1，邮箱是否已经被注册

    def validate_email(self, field):
        email =field.data
        # 只要数据库中第一次匹配成功就可以了
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

        # 在数据库中搜索一下，如果搜索到的话，就提示报错，否则正常注册

    # 2，验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # 如果查询，这个个字段都匹配的话
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()

        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或者验证码错误！")

        # 用完验证码后删除，后续改进使用redis
        # else:
        #     db.session.delete(captcha)
        #     db.session.commit()



# 登录逻辑的校验
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误，请重新输入！")])
    password = wtforms.StringField(validators=[Length(min=8, max=20, message="密码格式错误，8-20位")])


# 验证问答表单
class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误！！")])
    content = wtforms.StringField(validators=[Length(min=3, max=99999, message="内容过长或者太短！！！")])
