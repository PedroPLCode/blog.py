from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
   title = StringField('Title', validators=[DataRequired()])
   content = TextAreaField('Content', validators=[DataRequired()])
   is_published = BooleanField('Is Published?')