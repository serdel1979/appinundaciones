from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, RadioField, BooleanField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange


class ConfigurationForm(FlaskForm):

    private_primary_color_hex = TextField(
        'App Privado Primer Color', validators=[DataRequired()])
    private_secondary_color_hex = TextField(
        'App Privado Segundo Color', validators=[DataRequired()])
    private_terciary_color_hex = TextField(
        'App Privado Tercer Color', validators=[DataRequired()])
    public_primary_color_hex = TextField(
        'App Publico Primer Color', validators=[DataRequired()])
    public_secondary_color_hex = TextField(
        'App Publico Segundo Color', validators=[DataRequired()])
    public_terciary_color_hex = TextField(
        'App Publico Tercer Color', validators=[DataRequired()])
    num_elems = IntegerField(
        'Numero de elementos', validators=[DataRequired()])
    order_by = RadioField('Ordenar por', choices=[
                          (1,'Ascendiente'), (0, 'Descendiente')], validators=[DataRequired()])
    default = BooleanField('Cargar valores por defecto', id='default', default=False)
    submit = SubmitField('Save changes')
