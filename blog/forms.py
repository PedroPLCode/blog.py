from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Optional
from werkzeug.routing import ValidationError
from config import Config

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()])
    customcategory = StringField('Custom Category', validators=[Optional()])
    content = TextAreaField('Content', validators=[DataRequired()])
    is_published = BooleanField('Is Published?')
    
    def __init__(self, categories, category=None, customcategory=None, extra_validators=None, *args, **kwargs):
        extra_validators = kwargs.pop('extra_validators', None)
        super(EntryForm, self).__init__(*args, **kwargs)
        choices =  [category.name for category in categories] + ['new category']
        self.category.choices = choices
        self.extra_validators = extra_validators
            
        if customcategory:
            self.customcategory.data = customcategory


    def validate(self):
        if not super(EntryForm, self).validate():
            return False
        
        if self.extra_validators:
            for validator in self.extra_validators:
                if not validator(self):
                    return False

        if self.category.data == 'new category' and not self.customcategory.data:
            flash('Please enter the custom category.', 'warning')
            return False
        
        if self.category.data == 'new category':
            self.category.data = self.customcategory.data

        if not self.category.data and not self.customcategory.data:
            flash('Please select an category or enter a custom category.', 'warning')
            return False

        return True


    def is_customcategory_selected(self):
        return self.category.data == 'new category'

    
class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
   
   
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, field):
        return True if field.data == Config.ADMIN_USERNAME else False

    def validate_password(self, field):
        return True if field.data == Config.ADMIN_PASSWORD else False