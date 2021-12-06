 
from app.helpers.denuncias import CategoriaDenuncias
from marshmallow import Schema, fields, validate

phone = (r'(\d{0,5})\D*(\d{3,5})\D*(\d{3})\D*(\d{4})\D*(\d*)$')

def categorias(): 
    return [item.value for item in CategoriaDenuncias]
class ComplaintSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True)
    desc = fields.Str(required=True, validate=validate.Length(max=1999))
    category = fields.Int(required=True, validate=validate.OneOf(categorias()))
    latitude = fields.Str(required=True)
    longitude = fields.Str(required=True)
    surname = fields.Str()
    name = fields.Str(required=True)
    phone = fields.Str(required=True, validate=validate.Regexp(phone))
    email = fields.Email(required=True)
    status = fields.Int()
    user_id = fields.Int()
    


complaint_schema = ComplaintSchema()