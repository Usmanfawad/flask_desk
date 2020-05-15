from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField,IntegerField,widgets
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired,Length,EqualTo,ValidationError,Email,IPAddress,MacAddress
from ProDesk.models import *
from flask_wtf import widgets


class LoginForm(FlaskForm):
    email    = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    def validate_email(self,email):
        user = Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('This email is not registered.Please register or enter a correct email.')

def custom_validator():
    pass


class InventoryForm(FlaskForm):
    name            = StringField('Name',validators=[DataRequired()])
    ip_address      = StringField('Ip Address',validators=[IPAddress()])
    mac_address     = StringField('Mac Address',validators=[DataRequired()])
    purchase_date   = StringField('Purchase Date',validators=[DataRequired()])
    ageing_date     = StringField('Ageing Date',validators=[DataRequired()])
    # purchase_date   = DateField('Purchase date',validators=[DataRequired()],format='%Y/%m/%d')
    # ageing_date     = DateField('Ageing date',validators=[DataRequired()],format='%Y/%m/%d')
    submit = SubmitField('Submit form')

class MaterialUserForm(FlaskForm):
    f_name            = StringField('First name',validators=[DataRequired(),Length(min=1,max=30)])
    l_name            = StringField('Last name',validators=[DataRequired(),Length(min=1,max=30)])
    email             = StringField('Email',validators=[DataRequired(),Email()])
    number            = StringField('Number',validators=[DataRequired(),Length(min=1,max=30)])
    department        = StringField('Department')
    role              = SelectField("User Role",choices=[('ADMIN','Admin'),('USER','User')])
    submit= SubmitField('Submit form')

