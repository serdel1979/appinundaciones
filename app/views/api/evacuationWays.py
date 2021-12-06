from flask import jsonify, json, request
from app.views import blueprint
from app.models import Configuration, Way
from sqlalchemy.inspection import inspect



@blueprint.route('/api/recorridos-evacuacion/', methods=['GET'])
def recorridos_evacuacion():
    try:
        per_page = int(request.args.get("per_page", Configuration.get_num_elems()))
        page = int(request.args.get("page", 1))
        order_by  = 'name asc' if Configuration.is_ascendent() else 'name desc'
        paginado = Way.all(published=True, order_by=order_by).paginate(page, per_page, error_out=False)
        caminos = paginado.items
        total = paginado.total
        if not caminos:
            response = jsonify(
                status=404
            )
            return response,404
        else: 
            return jsonify({
                "Recorridos": [{"Coordenadas":[[p.latitude, p.longitude] for p in camino.points], "id": camino.id, "name": camino.name, "descripcion": camino.description} for camino in caminos],
                "Total" : total,
                "Pagina" : page
            })
    except:
        response = jsonify(
                status=501,
        )
        return response,501


@blueprint.route('/api/recorridos-evacuacion/<int:id>', methods=['GET'])
def recorrido(id):
    try:
        camino = Way.get_by_id(id=id)
        if not camino:
            response = jsonify(
                status=404,
            )
            return response,404
        else: 
            return jsonify(
                {"id": camino.id, "name": camino.name, "descripcion": camino.description,"Coordenadas":[[c.latitude,c.longitude] for c in camino.points]}
            )
    except:
        response = jsonify(
                status=501,
        )
        return response,501