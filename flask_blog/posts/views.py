from flask import render_template,url_for,flash,redirect,request,abort,Blueprint
from flask_blog.posts.forms import PostForm
from flask_blog.models import Post
from flask_blog import db
from flask_login import current_user,login_required
from flask_blog.utils import save_img_as

posts = Blueprint('posts',__name__)

@posts.route('/post/create',methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # handle post_image 
        post_img = form.post_img.data
        thumbnail_post_img = save_img_as(post_img,post=True,username=current_user.username) if post_img is not None else None
        post = Post(title=form.title.data,content=form.content.data,author=current_user,post_image=thumbnail_post_img)
        db.session.add(post)
        db.session.commit()
        flash(f'发布成功：{form.title.data}','primary')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='发布博客',form=form)

@posts.route('/post/<int:post_id>',methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=f'博客:{post.title}',post=post)

@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        flash('更新成功','success')
        return redirect(url_for('posts.post',post_id=post.id))
    if request.method == 'GET':
        form.post_img.data = post.post_image
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_post.html',title=f'更新博客:{post.title}',form=form)

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('删除成功','info')
    return redirect(url_for('main.home'))