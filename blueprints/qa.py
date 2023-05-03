from flask import Blueprint, request, render_template, g, redirect, url_for
from .froms import QuestionForm
from models import QuestionModel
from exts import db
from decorators import login_requested

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    # 将问答中的所有文件查询出来
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html', questions=questions)

@bp.route("/qa/public", methods=['GET', "POST"])
@login_requested

def public_question():
    # 判断如果没有登录的话跳转至登录页面
    # if not g.user:
    #     return redirect('/auth/login')

    # 下面使用装饰器来实现

    if request.method == 'GET':
        return render_template("public_question.html")

    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()

            # 之后跳转到这篇问答的详情页面，现在先跳转到首页
            # return 'hello world!'
            return redirect('/')
        else:
            print(form.errors)

            return redirect(url_for("qa.public_question"))


@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question =QuestionModel.query.get(qa_id)

    # 把查询到的内容返回到模板中
    return render_template("detail.html", question=question)

