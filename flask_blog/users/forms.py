from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_blog.models import User
# form base Class
class SelectField_Cn(SelectField):
    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v:
                break
        else:
            raise ValueError('无效选择，请重新选择')


class RegistrationForm(FlaskForm):
    username = StringField('账号',validators=[DataRequired('必填项'),Length(min=4,max=20,message='长度只能在4-20个字符之间')])
    email = StringField('邮箱',validators=[DataRequired('必填项'),Email('邮箱格式不对')])
    password = PasswordField('密码',validators=[DataRequired('必填项'),Length(min=6,max=20,message='长度只能在6-20个字符之间')])
    confirm_password = PasswordField('确认密码',validators=[DataRequired('必填项'),EqualTo('password','密码不一致'),Length(min=6,max=20,message='长度只能在6-20个字符之间')])
    submit = SubmitField('注册')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('这个账号已被注册')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('这个邮箱已被注册')
  
class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired('必填项'),Email('邮箱格式不对')])
    password = PasswordField('密码',validators=[DataRequired('必填项')])
    remember = BooleanField('记住账号')
    submit = SubmitField('登陆')

allowed_extensions = ['jpg','jpeg','png','gif']
sex_choices = (
    ('0','男'),
    ('1','女')
    )
class AccounForm(FlaskForm):
    sex = SelectField_Cn('性别',choices=sex_choices)
    biography = StringField('简介',validators=[Length(max=100,message='只允许0-100字符')])
    location = StringField('地址',validators=[Length(max=20,message='只允许20字符')])
    qq = StringField('QQ',validators=[Length(max=20,message='只允许20字符')])
    phone = StringField('电话号码',validators=[Length(max=11,message='手机格式不对')])
    avatar = FileField('上传头像',validators=[FileAllowed(allowed_extensions,message='只支持: '+'，'.join(allowed_extensions)+'格式')])
    # viewable = BooleanField('是否可见')
    submit = SubmitField('更新')

class RequestResetPasswordForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired('必填项'),Email('邮箱格式不对')])
    submit = SubmitField('发送邮箱验证')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('不存在这个邮箱')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码',validators=[DataRequired('必填项'),Length(min=6,max=20,message='长度只能在6-20个字符之间')])
    confirm_password = PasswordField('确认密码',validators=[DataRequired('必填项'),EqualTo('password','密码不一致'),Length(min=6,max=20,message='长度只能在6-20个字符之间')])
    submit = SubmitField('重置')