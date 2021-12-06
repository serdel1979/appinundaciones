from werkzeug.exceptions import BadRequest, Forbidden, InternalServerError
from app import db
from flask import jsonify, json, request, abort
from app.helpers.handler import validation_error
from app.views import blueprint
from app.models.complaint import Complaint
from app.models.config import Configuration
from app.schema.complaint_schema import ComplaintSchema, complaint_schema
from app.operations.complaint import CreateComplaint
from app.helpers.denuncias import CategoriaDenuncias, EstadoDenuncias
import re

"""

Api para denuncias


"""


@blueprint.route('/api/denuncias/', methods=['POST'])
def create():
    try:
        errors = ComplaintSchema().validate(request.get_json())
        if errors: 
            return validation_error(400, errors)
        new_complaint = CreateComplaint().new(**request.get_json())
        db.session.add(new_complaint)
        db.session.commit()
        result = complaint_schema.dump(new_complaint)
        return {"denuncia": result}, 201
    except BadRequest as e:
        abort(400)
    except InternalServerError as e: 
        abort(500)

@blueprint.route('/api/categories', methods=['GET'])
def get_categories():
       result = [ {"text": re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(item.name)), "value":item.value} for item in CategoriaDenuncias]
       return jsonify(result), 200


@blueprint.route('/api/denuncias/', methods=['GET'])
def get_denuncias():
    try:
        #per_page = request.args.get('limit', default = 1, type = int)
        per_page = int(request.args.get("per_page", Configuration.get_num_elems()))
        page = request.args.get('page', default = 1, type = int)
        order_by  = 'title asc' if Configuration.is_ascendent() else 'title desc'
        paginado = Complaint.all(order_by=order_by).paginate(page, per_page, error_out=False)
        denuncias = paginado.items
        total = paginado.total
        if not denuncias:
            abort(404)
        else: 
            return jsonify({"Denuncias": [{
                            "latlng": [den.latitude, den.longitude],
                            "id": den.id, 
                            "title": den.title,
                            "description": den.desc,
                            "category": re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", CategoriaDenuncias(den.category).name),
                            "status": re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", EstadoDenuncias(den.status).name),
                            "date": den.created_at
                            } for den in denuncias],
                "Total": total,
                "Page": page,
                "PerPage": per_page
            }), 200
    except:
        abort(501)
