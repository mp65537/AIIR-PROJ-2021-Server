from flask_wtf import FlaskForm
from wtforms import StringField, FileField

class CompileForm(FlaskForm):
    link = StringField('link')
    zip = FileField('zip')