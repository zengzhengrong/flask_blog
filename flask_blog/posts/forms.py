from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length

post_allowed_extensions = ['jpg','jpeg','png']
class PostForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired('必填项'),Length(max=100,message='只允许0-100字符')])
    content = TextAreaField('内容',validators=[DataRequired('必填项')])
    post_img = FileField('封面',validators=[FileAllowed(post_allowed_extensions,message='只支持: '+'，'.join(post_allowed_extensions)+'格式')])
    submit = SubmitField('发布')