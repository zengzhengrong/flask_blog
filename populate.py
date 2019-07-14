import time
from flask_blog.models import Post,User,Account
from flask_blog import create_app,bcrypt,db
app = create_app()
app.app_context().push()
posts = [
'C++',
'C#',
'C',
'Python',
'Java',
'go',
'ruby',
'shell',
'JavaScript',
'html5',
'css5',
'php',
'R',
'MATLAB',
'Perl',
'Objective-C',
'VB',
'sql',
'Swift',
'Lisp',
'Pascal',
'Ruby',
'SAS',
'Erlang',
'OpenCL'
]
users = [
    {
    'username':'admin',
    'email':'admin@163.com',
    'password':'admin123'
    },
    {
    'username':'zzr',
    'email':'zzr@163.com',
    'password':'zzr556689'
    },
    {
    'username':'jianbing',
    'email':'506862754@163.com',
    'password':'jianbing556689'
    }   
]
def populte():
    print('drop database')
    db.drop_all()
    print('drop done')
    print('create database')
    db.create_all()
    print('create database done')
    print('creating......')
    for user in users:
        hash_password = bcrypt.generate_password_hash(user.get('password')).decode('utf-8')
        create_user = User(username=user.get('username'),email=user.get('email'),password=hash_password)
        account = Account()
        create_user.account = account
        db.session.add(create_user)
        db.session.commit()
        print('create user success')
    print('create users done')
    admin = User.query.filter_by(username='admin').first()
    for post in posts:
        create_post = Post(title=post,content=post*3,author=admin)
        db.session.add(create_post)
        db.session.commit()
        print('create post success')
    print('done')  

if __name__ == '__main__':
    '''
    等待postgresql容器启动完毕
    '''
    while True:
        try:
            result = populte()
            if result is None:
                break
        except Exception as e:
            if 'could not connect to server' in str(e):
                print('正在等待postgresql容器启动完毕')
                time.sleep(2)
                continue
