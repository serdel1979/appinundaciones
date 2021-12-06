# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import widgets, TextField, PasswordField
from wtforms.fields.core import BooleanField, SelectMultipleField
from wtforms.validators import InputRequired, Email, DataRequired


class LoginForm(FlaskForm):
    username = TextField('Usuario', id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Contraseña', id='pwd_login',
                             validators=[DataRequired()])


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RolesForm(FlaskForm):
    roles = MultiCheckboxField('Roles', coerce=int)


class CreateAccountForm(RolesForm):
    username = TextField('Usuario', id='username_create',
                         validators=[DataRequired()])
    first_name = TextField(
        'Nombre', id='first_name', validators=[DataRequired()])
    last_name = TextField('Apellido', id='last_name',
                          validators=[DataRequired()])
    email = TextField('Email', id='email',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='password',
                             validators=[DataRequired()])
    active = BooleanField('Activo', id='active')

    retry_password = PasswordField('Password', id='retry_password',
                                   validators=[DataRequired()])


class CreateResetPasswordForm(FlaskForm):
    current_password = PasswordField('Contraseña actual', id='current_password',
                                     validators=[DataRequired()])
    password = PasswordField('Nueva contraseña', id='pwd_login',
                             validators=[DataRequired()])
    retry_password = PasswordField('Reitere contraseña', id='retry_password',
                                   validators=[DataRequired()])


class CreateSearchForm(FlaskForm):
    search = TextField('Ingrese usuario a buscar', id='search')
    active = BooleanField('Mostrar usuarios inactivos', id='active')


class CreateSearchZoneForm(FlaskForm):
    search = TextField('Ingrese zona a buscar', id='search')
    active = BooleanField('Mostrar zonas despublicadas', id='active')


class CreateSearchWayForm(FlaskForm):
    search = TextField('Ingrese un camino a buscar', id='search')
    active = BooleanField('Mostrar caminos despublicadas', id='active')


class CreateWayForm(FlaskForm):
    name = TextField('Nombre', id='name',
                     validators=[DataRequired()])
    description = TextField(
        'Descripción', id='descripcion', validators=[DataRequired()])
    search = TextField('Ingrese un camino a buscar', id='search')
    active = BooleanField('Mostrar caminos despublicadas', id='active')
