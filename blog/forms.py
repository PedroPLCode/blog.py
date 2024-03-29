from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.routing import ValidationError
from config import Config

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    is_published = BooleanField('Is Published?')
   
   
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, field):
        return True if field.data == Config.ADMIN_USERNAME else False

    def validate_password(self, field):
        return True if field.data == Config.ADMIN_PASSWORD else False