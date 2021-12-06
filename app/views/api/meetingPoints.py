from flask import jsonify, json, request
from app.views import blueprint
from app.models import Configuration, Location
from sqlalchemy.inspection import inspect



@blueprint.route('/api/puntos-encuentro/', methods=['GET'])
def meetingPoints():
    try:
        per_page = int(request.args.get("per_page", Configuration.get_num_elems()))
        page = int(request.args.get("page", 1))
        order_by  = 'name asc' if Configuration.is_ascendent() else 'name desc'
        paginado = Location.all_locations(order_by=order_by, published=True).paginate(page, per_page, error_out=False)
        puntos = paginado.items
        total = paginado.total
        if not puntos:
            response = jsonify(
                status=404
            )
            return response,404
        else: 
            return jsonify({
                "Puntos_encuentro": [{ "id": punto.id, "name": punto.name, "dirección": punto.address, "latlong": [punto.latitude , punto.longitude] ,"teléfono":punto.telephone,"email": punto.email } for punto in puntos],
                "Total" : total,
                "Pagina" : page
            })
    except:
        response = jsonify(
                status=501,
        )
        return response,501


