
#zonas_inundacion

import datetime
from flask.globals import session
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from flask.helpers import flash
from app.forms import CreateSearchZoneForm
from app.views import blueprint
from flask import render_template, redirect, url_for, request
from app.models import User, Role, Configuration, Zone
from app.helpers.util import verify_pass, hash_pass
from app.helpers.decorators import user_has
import json
import csv
import io


## Login & Registration


@blueprint.route('/zonas', methods=['GET', 'POST'])
@login_required
@user_has('zona_index')
def zonas():
    searchzoneform = CreateSearchZoneForm(request.form)
    per_page = Configuration.get_num_elems()
    if request.form.get('file-input'):
        upload_zonas()
    # del campo hidden del template
    page = request.form.get('page')
    current_page = int(page) if page else 1
    zonename = request.form.get('search')
    active = bool(request.form.get('active'))
    order_by = 'name asc' if Configuration.is_ascendent() else 'name desc'

    if zonename != None:
        encontrados = Zone.by_name(zonename, not active, order_by).paginate(
            current_page, per_page, error_out=False)
    else:
        encontrados = Zone.all(not active, order_by).paginate(
            current_page, per_page, error_out=False)
    return render_template("zones/zones.html", zonas=encontrados, form=searchzoneform)


def upload_zonas():
    print('llega')


@blueprint.route('/zonas/<int:id>/toggle-status')
@login_required
@user_has('zona_update')
def publicar_despublicar_zona(id):
    zona = Zone.get_by_id(id)
    if not zona:
        flash("Zona inexistente", "error")
    zona.toggle()
    if zona.published:
        flash("Zona publicada exitosamente", "success")
    else:
        flash("Zona despublicada exitosamente", "success")
    return redirect(url_for("blueprint.zonas"))




@blueprint.route('/zoneview/<int:id>', methods=['GET'])
# TODO:solo el admin deberia poder
@login_required
@user_has('zona_show')
def zone_view(id):
    zona = Zone.get_by_id(id)
    coordenadas = zona.get_polygon()
    lat = coordenadas[0][0]
    long = coordenadas[0][1]
    return render_template('zones/zone-view.html', zona=zona, polygon=map(json.dumps, coordenadas), lat = lat, long = long)
    

@blueprint.route('/zone_delete/<int:id>', methods=['GET'])
# TODO:solo el admin deberia poder
@login_required
@user_has('zona_destroy')
def zone_delete(id):
    Zone.delete(id)
    return redirect(url_for("blueprint.zonas"))

@blueprint.route('/upload_zonas', methods=['POST'])
# TODO:solo el admin deberia poder
@login_required
@user_has('zona_import')
def upload_zonas():
  try:    
    with io.TextIOWrapper(request.files["file-input[]"], encoding="latin-1", newline='\n') as text_file:
        reader = csv.reader(text_file, delimiter=';')
        lista = list(reader)
        primer = True
        for l in lista:
            if not primer:  #ignora la primer fila del archivo
                for ll in l:    #se recorre el contenido de cada fila
                    lineaFinal = ll.split(sep="\"")
                    zona = None     #inicializa valores para guardar la fila actual
                    nombreZona=""
                    coordenadas = None  
                    for i in range(len(lineaFinal)):    #se recorre la fila
                        if (i % 2 == 0)and(i != 2):         #se analiza si es el nombre o son las coordenadas, si es par es el nombre
                            nombreZona = lineaFinal[i]
                            nam = nombreZona[:-1]               #elimino la coma del final
                            zonaBuscada = Zone.get_by_name(nam) #busco una zona con ese nombre para ver si ya existe
                            if zonaBuscada:                        #si existe guardo la zona
                                zona = zonaBuscada    
                            else:
                                zona = Zone(name=nam, colour = "#FF00EE", published = True)  #si no existe, creo una zona nueva
                        else:
                            if i != 2:
                                coordenadas = lineaFinal[i]         #si no es el nombre y no es el indice 2 que no se usa, guardo las coordenadas
                        if zona is not None and coordenadas is not None and nombreZona != "":
                            zona.set_polygon(coordenadas)           #si los valores fueron inicializados correctamente, seteo las coordenadas al poligono de la zona
            else:
                primer = False
    flash("Carga exitosa","succes")
    return redirect(url_for("blueprint.zonas"))
  except:
    flash("Error al importar archivo","error")
    return redirect(url_for("blueprint.zonas"))

