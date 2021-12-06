from flask.globals import session
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from flask.helpers import flash
from app.forms import CreateSearchWayForm, CreateWayForm
from app.models.evacuation import Way, WayPoint
from app.views import blueprint
from flask import render_template, redirect, url_for, request
from app.models import User, Role, Configuration, Zone
from app.helpers.util import verify_pass, hash_pass
from app.helpers.decorators import user_has
import json


## Login & Registration


@blueprint.route('/way_list', methods=['GET', 'POST'])
@login_required
@user_has('evacuacion_index')
def way_list():
    searchwayform = CreateSearchWayForm(request.form)
    per_page = Configuration.get_num_elems()

    # del campo hidden del template
    page = request.form.get('page')
    current_page = int(page) if page else 1
    wayname = request.form.get('search')
    active = bool(request.form.get('active'))
    order_by = 'name asc' if Configuration.is_ascendent() else 'name desc'

    if wayname != None:
        encontrados = Way.by_name(wayname, not active, order_by).paginate(
            current_page, per_page, error_out=False)
    else:
        encontrados = Way.all(not active, order_by).paginate(
            current_page, per_page, error_out=False)
    return render_template("evacuation/way_list.html", ways=encontrados, form=searchwayform)



@blueprint.route('/way/<int:id>/toggle-status')
@login_required
@user_has('evacuacion_update')
def publicar_despublicar_camino(id):
    way = Way.get_by_id(id)
    if not way:
        flash("Camino inexistente", "error")
    way.toggle()
    if way.published:
        flash("Camino publicado exitosamente", "success")
    else:
        flash("Camino despublicado exitosamente", "success")
    return redirect(url_for("blueprint.way_list"))




@blueprint.route('/wayview/<int:id>', methods=['GET'])
# TODO:solo el admin deberia poder
@login_required
@user_has('evacuacion_show')
def way_view(id):
    way = Way.get_by_id(id)
    coordenadas = way.get_points()
    lat = coordenadas[0][0]
    long = coordenadas[0][1]
    return render_template('evacuation/way_view.html', way=way, linea=map(json.dumps, coordenadas), lat = lat, long = long)



@blueprint.route('/wayedit/<int:id>', methods=['GET'])
# TODO:solo el admin deberia poder
@login_required
@user_has('evacuacion_update')
def way_edit(id):
    way = Way.get_by_id(id)
    coordenadas = way.get_points()
    lat = coordenadas[0][0]
    long = coordenadas[0][1]
    return render_template('evacuation/way_edit.html', nombre= way.name, descripcion = way.description , published = way.published,linea=map(json.dumps, coordenadas), lat = lat, long = long)


@blueprint.route('/way_add', methods=['GET', 'POST'])
@login_required
@user_has('evacuacion_create')
def way_add():
    create_way = CreateWayForm(request.form)
    if "addway" in request.form:
        name=request.form["name"]
        way = Way.get_by_name(name)
        if way:
            flash("El nombre ya está en uso", 'error')
            return redirect(url_for("blueprint.way_list"))
        name=request.form["name"]
        descripcion=request.form["description"]
        return render_template('evacuation/select_points.html', name=name, descripcion=descripcion)
    else:
        return render_template('evacuation/way_add.html', form=create_way)




@blueprint.route('/way_save/', methods=['POST'])
@login_required
@user_has('evacuacion_create')
def way_save():
    try:
        name=request.form["name"]
        descripcion = request.form["description"]
        ruta = Way(name=name, description = descripcion, published = True)
        points = request.form["inputjson"]
        puntos = points.split(sep=",")
        caracteres = "[]\""
        lat=""
        lng=""
        for i in range(len(puntos)):
            if i % 2 == 0:
                lat = ''.join( x for x in puntos[i] if x not in caracteres)
            else:
                lng = ''.join( x for x in puntos[i] if x not in caracteres)
                coordenadas = WayPoint(latitude=lat, longitude=lng,route = ruta)
                coordenadas.save()
        ruta.save()
    except:
        flash("No se pudo guardar", 'error')
        print("error")
    return redirect(url_for("blueprint.way_list"))


@blueprint.route('/way_save_edit/', methods=['POST'])
@login_required
@user_has('evacuacion_update')
def way_save_edit():
  
        name=request.form.get("name", False)
        descripcion=request.form.get("description", False)
        ruta = Way.get_by_name(name)
        ruta.set_description(description = descripcion)
        points = request.form["inputjson"]
        if points != "":
            ruta.delete_points()
            puntos = points.split(sep=",")
            caracteres = "[]\""
            lat=""
            lng=""
            for i in range(len(puntos)):
                if i % 2 == 0:
                    lat = ''.join( x for x in puntos[i] if x not in caracteres)
                else:
                    lng = ''.join( x for x in puntos[i] if x not in caracteres)
                    coordenadas = WayPoint(latitude=lat, longitude=lng,route = ruta)
                    coordenadas.save()
        ruta.save()
        flash("Actualizado", 'succes')
        return redirect(url_for("blueprint.way_list"))


@blueprint.route('/way_delet/<int:id>', methods=['GET'])
# TODO:solo el admin deberia poder
@login_required
@user_has('evacuacion_destroy')
def way_delet(id):
    Way.delete(id)
    return redirect(url_for("blueprint.way_list"))
    