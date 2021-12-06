from flask.helpers import flash
from app.helpers.decorators import user_has
from app.models import Configuration, Location
from app.models.location import Coordinate
from app.views import blueprint
from app.forms import LocationForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required
from flask import jsonify



@blueprint.route('/location_list', methods=['POST', 'GET'])
@login_required
@user_has('punto_encuentro_index')
def location_list():
    per_page = Configuration.get_num_elems()
    order_by = 'name asc' if Configuration.is_ascendent() else 'name desc'

    unpublished = bool(request.form.get('unpublished'))

    # del campo hidden del template
    page = request.form.get('page')
    current_page = int(page) if page else 1

    search_location = request.form.get('search')
    if search_location:
        locs = Location.search_location(search_location, order_by, not unpublished).paginate(
            current_page, per_page, error_out=False)
    else:
        locs = Location.all_locations(order_by, not unpublished).paginate(
            current_page, per_page, error_out=False)
    if not len(locs.items) and search_location:
        flash("No hubo coincidencias en su búsqueda", "warning")

    return render_template("locations/location-list.html", locations=locs, unpublished=unpublished)


@blueprint.route('/locations/<int:id>/', methods=['GET'])
@login_required
@user_has('punto_encuentro_show')
def location_view(id):
    loc = Location.get_by_id(id)
    return render_template('locations/location-view.html', loc=loc)


@blueprint.route('/locations/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@user_has('punto_encuentro_update')
def location_edit(id):
    loc = Location.get_by_id(id)
    form = LocationForm(obj=loc)

    if form.is_submitted():
        if form.validate():
            form.populate_obj(loc)
            loc.save()
            flash("cambios registrados con éxito", 'success')
            return redirect(url_for('blueprint.location_list'))
        return redirect(url_for('blueprint.location_edit', id=id))
    return render_template('locations/location-edit.html', form=form, id=id)


@blueprint.route('/locations/register', methods=['GET', 'POST'])
@login_required
@user_has('punto_encuentro_new')
def register_location():
    form = LocationForm()
    if form.is_submitted():
        if form.validate():
            location = Location()
            form.populate_obj(location)  # Copies matching attributes from form onto location
            location.save()
            flash("Punto de encuentro creado exitosamente", 'success')
            return redirect(url_for('blueprint.location_list'))
        return redirect(url_for('blueprint.register_location'))
    return render_template('locations/add_location.html', form=form)


@blueprint.route('/locations/<int:id>/delete')
@login_required
@user_has('punto_encuentro_destroy')
def delete_location(id):
    Location.delete(id)
    flash("Punto de encuentro eliminado satisfactoriamente", "success")
    return redirect(url_for("blueprint.location_list"))


@blueprint.route('/locations/all/coordinates', methods=['GET'])
@login_required
@user_has('punto_encuentro_show')
def location_coordinates():
    locations = Location.all()
    list = []
    for loc in locations:
        list.append(Coordinate(latitude=loc.latitude, longitude=loc.longitude))
    return jsonify(results=list)
