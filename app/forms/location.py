from app.models import Location
from flask_wtf import FlaskForm
from wtforms import TextField, RadioField
from wtforms.validators import DataRequired, Email, ValidationError
from flask.helpers import flash


class LocationForm(FlaskForm):

    name = TextField(
        'Name', validators=[DataRequired()])
    address = TextField(
        'Address', validators=[DataRequired()])
    latitude = TextField(
        'latitude', validators=[DataRequired()])
    longitude = TextField(
        'longitude', validators=[DataRequired()])
    status = RadioField('Status', choices=[
        ('publicado'), ('despublicado')], default='publicado')
    telephone = TextField(
        'Telephone', validators=[DataRequired()])
    email = TextField(
        'Email', validators=[Email()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orig = kwargs.get('obj', None)

    def validate_name(self, name):
        if self.orig is None or name.data != self.orig.name:
            loc = Location.query.filter_by(name=self.name.data).first()
            if loc is not None:
                flash("El nombre ya se encuentra registrado", 'error')
                raise ValidationError()

    def validate_address(self, address):
        if self.orig is None or address.data != self.orig.address:
            loc = Location.query.filter_by(address=self.address.data).first()
            if loc is not None:
                flash("La dirección ya se encuentra registrada", 'error')
                raise ValidationError()

    def validate_telephone(self, telephone):
        if self.orig is None or telephone.data != self.orig.telephone:
            loc = Location.query.filter_by(
                telephone=self.telephone.data).first()
            if loc is not None:
                flash("El teléfono ya se encuentra registrado", 'error')
                raise ValidationError()

    def validate_email(self, email):
        if self.orig is None or email.data != self.orig.email:
            loc = Location.query.filter_by(email=self.email.data).first()
            if loc is not None:
                flash("El email ya se encuentra registrado", 'error')
                raise ValidationError()

    def validate_latitude(self, latitude):
        length = len(latitude.data)
        if length < 4 or length > 30:
            flash("Latitud - Ingrese valor entre 4 y 30 dígitos", 'error')
            raise ValidationError()

    def validate_longitude(self, longitude):
        length = len(longitude.data)
        if length < 4 or length > 30:
            flash("Longitud - Ingrese valor entre 4 y 30 dígitos", 'error')
            raise ValidationError()
