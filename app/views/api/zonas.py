from flask import Flask
from flask import jsonify, json, request
from app.views import blueprint
from app.models import Configuration, Zone
from sqlalchemy.inspection import inspect



@blueprint.route('/api/zonas-inundables/', methods=['GET'])
def zones():
        per_page = int(request.args.get("per_page", Configuration.get_num_elems()))
        page = int(request.args.get("page", 1))
        order_by  = 'name asc' if Configuration.is_ascendent() else 'name desc'
        paginado = Zone.all(published=True, order_by=order_by).paginate(page, per_page, error_out=False)
        zonas = paginado.items
        total = paginado.total
        if not zonas:
            response = jsonify(
                status=404
            )
            return response,404
        else: 
            return jsonify({
                "Zonas": [{"Coordenadas":[[p.latitude, p.longitude] for p in zona.polygon], "id": zona.id, "name": zona.name, "colour": zona.colour} for zona in zonas],
                "Total" : total,
                "Pagina" : page
            })

        response = jsonify(
                status=501,
        )
        return response,501


@blueprint.route('/api/zonas-inundables/<int:id>', methods=['GET'])
def zone(id):
    try:
        zona = Zone.get_by_id(id=id)
        if not zona:
            response = jsonify(
                status=404,
            )
            return response,404
        else: 
            return jsonify(
                {"id": zona.id, "name": zona.name, "colour": zona.colour,"Coordenadas":[[p.latitude,p.longitude] for p in zona.polygon]}
            )
    except:
        response = jsonify(
                status=501,
        )
        return response,501