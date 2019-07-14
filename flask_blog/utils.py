import os 
import secrets
from PIL import Image
from flask_blog import mail
from flask_mail import Message
from flask import current_app

def save_img_as(img,post=None,username=None):
    '''
    Get the img and save as \n
    Use secrets module to rename img 
    '''
    random_hex = secrets.token_hex(8)
    _, f_extensions = os.path.splitext(img.filename)
    rename_img = random_hex + f_extensions # 空二进制图像文件
    if post is None:
        avatar_path = 'static/account/avatar/'
        avatar_fullpath = current_app.root_path + '/static/account/avatar/'
        if not os.path.exists(avatar_fullpath):
            os.makedirs(avatar_fullpath)
        save_fullpath = os.path.join(current_app.root_path,avatar_path,rename_img)
    if post and username:
        post_path = f'static/posts/{username}/'
        # print(current_app.root_path)
        post_fullpath = current_app.root_path + f'/static/posts/{username}/'
        if not os.path.exists(post_fullpath):
            os.makedirs(post_fullpath)
        save_fullpath = os.path.join(current_app.root_path,post_path,rename_img)
    if f_extensions == '.gif':
        img.save(save_fullpath)
        return rename_img
    # PIL 处理png jpg jpeg图像生成缩略图
    resize = (125,125)
    avatar = Image.open(img)
    avatar.thumbnail(resize)
    avatar.save(save_fullpath) # 另存为
    return rename_img

def send_reset_email(rec,token,reset_link):
    print(os.environ.get('EMAIL_USER'))
    print(os.environ.get('EMAIL_PASSWORD'))
    message = Message("[zzr's blog]密码重置验证",sender='bhg889@163.com',recipients=[rec])
    message.body = f"""
    点击下面的链接重置你的密码:
    {reset_link}
    如果不是你发出的重置请求，请忽略该邮件
    """
    mail.send(message)
    return True