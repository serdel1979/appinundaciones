
from werkzeug.exceptions import BadRequest, Forbidden, InternalServerError
from app import db
from flask import jsonify, json, request, abort
from app.helpers.handler import validation_error
from app.views import blueprint
from app.models.config import Configuration



@blueprint.route('/api/config/', methods=['GET'])
def get_public_colors():
    try:
        public_colors =  Configuration.get_public_app()
        if not public_colors:
            abort(404)
        else: 
            return jsonify(public_colors), 200
    except:
        abort(501)