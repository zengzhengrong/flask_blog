from datetime import datetime,timedelta
from flask import current_app
from flask_blog import db,login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

cn_timezone = datetime.utcnow() + timedelta(hours=8)

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(12),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    image_file = db.Column(db.String(20),nullable=True,default='default.jpg')
    posts = db.relationship('Post',backref='author',lazy=True)
    account = db.relationship('Account',backref='user',lazy=True,uselist=False)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    def generate_rest_token(self,expired_sec=600):
        serializer = Serializer(current_app.config['SECRET_KEY'],expires_in=expired_sec)
        return serializer.dumps({'user_id':self.id}).decode('utf-8')
    @staticmethod
    def verify_rest_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id'] # 只获取id
        except:
            return None
        return User.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    created_time = db.Column(db.DateTime,nullable=False,default=cn_timezone)
    update_time = db.Column(db.DateTime,nullable=True)
    post_image = db.Column(db.String(20),nullable=True,default='default.jpg')
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f"Post('{self.title}','{self.author.username}','{self.created_time}')"

class Account(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    biography = db.Column(db.String(100))
    location = db.Column(db.String(20))
    phone = db.Column(db.String(11))
    qq = db.Column(db.String(20))
    # github = db.Column(db.String(100),default='github.com/zengzhengrong')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    created_time = db.Column(db.DateTime,nullable=False,default=cn_timezone)
    # viewable = db.Column(db.Boolean,default=True)
    sex = db.Column(db.String(10),default=None)
    def __repr__(self):
        return f"UserAccount('{self.user.username}','{self.phone}','{self.created_time}')"