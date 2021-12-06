from flask_wtf import FlaskForm
from wtforms import TextField,  SubmitField, TextAreaField, HiddenField,StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import SelectField
from wtforms.validators import InputRequired, Email, DataRequired, Optional, ValidationError, Length
import phonenumbers
from app.helpers.denuncias import EstadoDenuncias, CategoriaDenuncias
from app.models.user import User

def user_query():
    return User.query.all()

class FollowUpForm(FlaskForm):
    description = TextAreaField('Descripcion',
                         validators=[DataRequired(), Length(min=5, max=2000)])
    author_id = QuerySelectField('Operario', validators=[InputRequired(u'Por favor elegir un usuario')],
                               query_factory=user_query, get_label='username')

    submit = SubmitField('Guardar seguimiento')
class ComplaintForm(FlaskForm):
    title = TextField('Titulo',
                      validators=[DataRequired(), Length(min=1, max=30)])
    desc = TextAreaField('Descripcion',
                         validators=[DataRequired(), Length(min=5, max=2000)])
    name = TextField('Nombre',
                     validators=[DataRequired()])
    surname = TextField('Apellido')
    email = StringField('Email', id='email',
                      validators=[DataRequired(), Email(u"Por favor ingresar un email")])
    latitude = HiddenField(
        'latitude', id="lat")
    longitude = HiddenField(
        'longitude', id="lng")
    status = SelectField('Status', choices=[item.name for item in EstadoDenuncias])
    category = SelectField('Categoría', choices=[item.name for item in CategoriaDenuncias])
    phone = TextField(
        'Telefono', validators=[DataRequired()])
    user_id = QuerySelectField('Operario responsable',allow_blank = True,
                               query_factory=user_query, validators=[Optional(strip_whitespace=True)], get_label='username',
                               )
    submit = SubmitField('Guardar denuncia')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data, 'AR')
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Numero de telefono es invalido')



class ComplaintSearchForm(FlaskForm):
    search = TextField('Ingrese titulo de denuncia a buscar', id='title')
    date_range = TextField('Ingrese rango de fecha', id="date_range", render_kw={'readonly': True})
    range_from = HiddenField("range_from")
    range_to = HiddenField("range_to")
    criteria = SelectField('Criterio de filtro', id='criteria',
                           choices=[('select_options', 'Seleccione criterio de filtro'), ('title', 'Título'), ('date_range', 'Rango de fechas'),
                                    ('status', 'Estado')], default="select_options"
                           )

    status = SelectField('Mostrar denuncias por estado', id='status',
                         choices=[(str(EstadoDenuncias.EnCurso.value), str(EstadoDenuncias.EnCurso.name)), 
                         (str(EstadoDenuncias.Resuelta.value), str(EstadoDenuncias.Resuelta.name)), 
                         (str(EstadoDenuncias.Cerrada.value), str(EstadoDenuncias.Cerrada.name)), ('-1', 'Todas')],
                         default=-1)
