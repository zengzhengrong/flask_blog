from flask import render_template,request,Blueprint
from flask_blog.models import Post


main = Blueprint('main',__name__)

@main.route('/')
@main.route('/home')
def home():
    get_current_page = request.args.get('page',1,type=int) # defalut page num = 1
    posts = Post.query.order_by(Post.created_time.desc()).paginate(page=get_current_page,per_page=5)
    # print(len(posts))
    return render_template('home.html',posts=posts,title='flask_zzr')