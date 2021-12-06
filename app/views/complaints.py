# -*- encoding: utf-8 -*-
from flask import json
from flask.globals import session
from flask.json import jsonify
from app.helpers.denuncias import EstadoDenuncias, CategoriaDenuncias
from app.schema.complaint_schema import ComplaintSchema, complaint_schema
from flask_login.utils import login_required
from app.views import blueprint
from flask import render_template, request, url_for, redirect, flash, abort
from app.models import Configuration
from app.models.complaint import Complaint, FollowUp
from app.forms.complaint import ComplaintForm, ComplaintSearchForm, FollowUpForm
from app.operations.complaint import CreateComplaint
from app.helpers.decorators import user_has
import logging

logger = logging.getLogger(__name__)
# Hey, wait, I got a new Complaint


"""
Cargo una nueva denuncia
"""


@blueprint.route('/denuncias/new', methods=['GET', 'POST'])
@login_required
@user_has('complaint_create')
def nueva_denuncia():
    form = ComplaintForm(request.form)
    if form.is_submitted():
        if form.validate():
            complaint = dict(
                title=request.form.get('title'),
                desc=request.form.get('desc'),
                latitude=request.form.get('latitude'),
                longitude=request.form.get('longitude'),
                surname=request.form.get('surname'),
                name=request.form.get('name'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                category=CategoriaDenuncias[request.form.get(
                    'category')].value,
            )

            errors = complaint_schema.validate(complaint)
            if errors:
                flash(
                    f"Hay errores en los valores del formulario: {errors}", "error")
                return redirect(url_for('blueprint.nueva_denuncia'))
            else:
                new_complaint = CreateComplaint.new(**complaint)
                new_complaint.update_status(
                    EstadoDenuncias[request.form.get('status')].value)
                if (request.form.get('user_id')) != '__None':
                    new_complaint.add_user(user=request.form.get('user_id'))
                new_complaint.save()
                flash("cambios registrados con éxito", "success")
            return redirect(url_for('blueprint.denuncias_list'))

    return render_template('complaints/new-complaint.html', form=form)


"""
Ruta para ver una denuncia determinada
"""


@blueprint.route('/denuncias/<int:id>/view', methods=['POST', 'GET'])
@login_required
@user_has('complaint_show')
@user_has('followup_index')
def denuncia_view(id):
    complaint = Complaint.get_by_id(id)
    page = request.form.get('page')
    per_page = Configuration.get_num_elems()
    current_page = int(page) if page else 1

    order_by = 'id asc' if Configuration.is_ascendent() else 'id desc'

    follow_ups = FollowUp.get_follow_ups_for_complaint(
        id, order_by).paginate(current_page, per_page, error_out=False)
    return render_template('complaints/view-complaint.html', complaint=complaint, followups=follow_ups, stat=EstadoDenuncias, cat=CategoriaDenuncias)


"""
Rutas para editar una denuncia determinada (solo admin)
"""


@blueprint.route('/denuncias/<int:id>/edit', methods=['GET'])
@login_required
@user_has('complaint_update')
def edit_complaint(id):
    complaint = Complaint.get_by_id(id)
    form = ComplaintForm(obj=complaint)
    return render_template('complaints/new-complaint.html', den=complaint, form=form)


@blueprint.route('/denuncias/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@user_has('complaint_update')
def update_complaint(id):
    complaint = Complaint.get_by_id(id)
    form = ComplaintForm(obj=complaint)
    if form.is_submitted():
        if not form.validate():
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(
                        f"Hay errores en el formulario, {fieldName}: {err}", "error")
            return redirect(url_for('blueprint.update_complaint', id=complaint.id))
        else:
            data = dict(
                title = request.form.get('title'),
                desc = request.form.get('desc'),
                latitude = request.form.get('latitude'),
                longitude = request.form.get('longitude'),
                surname = request.form.get('surname'),
                name = request.form.get('name'),
                phone = request.form.get('phone'),
                email = request.form.get('email'),
                category = CategoriaDenuncias[request.form.get('category')].value,
                status = int(EstadoDenuncias[request.form.get('status')].value)
                )
            logger.warning(request.form.get('longitude'))
            errors = complaint_schema.validate(data)
            if errors:
                flash(
                    f"Hay errores en los valores del formulario: {errors}", "error")
                return redirect(url_for('blueprint.update_complaint', id=complaint.id))
            else:
                if (request.form.get('user_id')) != '__None':
                    complaint.set_user(user=request.form.get('user_id'))
                if EstadoDenuncias[request.form.get('status')].value == EstadoDenuncias.Cerrada.value:
                    complaint.close_complaint()
                else:
                    complaint.closed_date = None
                complaint.update(**data)
                complaint.save()
                flash("cambios registrados con éxito", "success")
                return redirect(url_for('blueprint.denuncias_list'))
    return render_template('complaints/new-complaint.html', den=complaint, form=form)


"""
Ruta que muestra el listado de denuncas en app privada
"""


@blueprint.route('/denuncias/', methods=['POST', 'GET'])
@login_required
@user_has('complaint_index')
def denuncias_list():
    searchform = ComplaintSearchForm(request.form)
    per_page = Configuration.get_num_elems()

    # del campo hidden del template
    page = request.form.get('page')

    print('range', request.form.get('range_from'))
    current_page = int(page) if page else 1

    criterial = request.form.get('criteria')

    values = []
    order_by = 'title asc' if Configuration.is_ascendent() else 'title desc'

    if criterial != None:
        if criterial == 'title':
            if not request.form.get('search'):
                values = Complaint.all(order_by).paginate(
                    current_page, per_page, error_out=False)
            else:
                values = Complaint.find_by_title(request.form.get('search'), order_by).paginate(
                    current_page, per_page, error_out=False)
        elif criterial == 'status':
            if int(request.form.get('status')) != -1:
                values = Complaint.find_by_status(request.form.get('status'), order_by) \
                    .paginate(current_page, per_page, error_out=False)
            else:
                values = Complaint.all(order_by).paginate(
                    current_page, per_page, error_out=False)
        else:
            if request.form.get('range_from') != "":
                values = Complaint.find_by_created_at_range(request.form.get('range_from'), request.form.get(
                    'range_to'), order_by).paginate(current_page, per_page, error_out=False)
            else:
                values = Complaint.all(order_by).paginate(
                    current_page, per_page, error_out=False)
    else:
        values = Complaint.all(order_by).paginate(
            current_page, per_page, error_out=False)

    return render_template('complaints/complaints.html', complaints=values, form=searchform, stat=EstadoDenuncias, cat=CategoriaDenuncias)


"""
Ruta para borrar una denuncia determinada (solo admin)
"""


@blueprint.route('/denuncias/<int:id>/delete', methods=['GET', 'DELETE'])
@login_required
@user_has('complaint_destroy')
def delete_complaint(id):
    Complaint.delete(id)
    flash("Denuncia eliminada con éxito", "success")
    return redirect(url_for('blueprint.denuncias_list'))


"""
Ruta para cerrar una denuncia determinada (solo admin)
"""


@blueprint.route('/denuncias/<int:id>/close', methods=['GET', 'POST'])
@login_required
@user_has('complaint_update')
@user_has('followup_create')
def cerrar_denuncia(id):
    complaint = Complaint.get_by_id(id)
    complaint.close_complaint()
    complaint.save()
    followup = FollowUp(
                description= "No fue posible contactar al denunciante",
                author_id= session["id"],
                complaint_id=id)
    followup.save()
    flash("Denuncia cerrada con éxito", "success")
    return redirect(url_for('blueprint.denuncias_list'))


"""
Ruta para crear un seguimiento nuevo
"""


@blueprint.route('/denuncias/<int:complaint_id>/followup/new', methods=['GET', 'POST'])
@login_required
@user_has('followup_create')
def new_followup(complaint_id):
    form = FollowUpForm(request.form)
    if form.is_submitted():
        if form.validate():
            followup = FollowUp(
                description=request.form.get('description'),
                author_id=request.form.get('author_id'),
                complaint_id=complaint_id)
            followup.save()
            flash("cambios registrados con éxito", "success")
            return redirect(url_for('blueprint.denuncia_view', id=complaint_id))
        else:
            flash("errores en el formulario", "error")
            return redirect(url_for('blueprint.new_followup', id=complaint_id))
    return render_template('complaints/followups/new_followup.html', form=form, id=complaint_id)


"""
Rutas para editar un seguimiento determinado
"""


@blueprint.route('/denuncias/<int:complaint_id>/followup/<int:id>/edit', methods=['GET'])
@login_required
@user_has('followup_update')
def edit_followup(complaint_id, id):
    follow_up = FollowUp.get_by_id(id)
    form = FollowUpForm(obj=follow_up)

    return render_template('complaints/followups/new_followup.html', form=form, id=complaint_id, fol=follow_up)


@blueprint.route('/denuncias/<int:complaint_id>/followup/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@user_has('followup_update')
def update_followup(complaint_id, id):
    follow_up = FollowUp.get_by_id(id)
    form = FollowUpForm(obj=follow_up)
    logger.warning(f'{follow_up}')
    if form.is_submitted():
        if form.validate():
            follow_up.update(
                description=request.form.get('description'),
                author_id=request.form.get('author_id'),
                complaint_id=complaint_id
            )
            follow_up.save()
            flash("cambios registrados con éxito", "success")
            return redirect(url_for('blueprint.denuncia_view', id=complaint_id))
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f"Hay errores en el formulario, {fieldName}: {err}", "error")
            return redirect(url_for('blueprint.update_followup', complaint_id=complaint_id, id=id))
    return render_template('complaints/followups/new_followup.html', form=form, id=complaint_id, fol=follow_up)


"""
Rutas para eliminar un seguimiento determinado
"""


@blueprint.route('/denuncias/<int:complaint_id>/followup/<int:id>/delete', methods=['GET', 'DELETE'])
@user_has('followup_destroy')
@login_required
def delete_followup(complaint_id, id):
    FollowUp.delete(id)
    flash("Seguimiento eliminado con éxito", "success")
    return redirect(url_for('blueprint.denuncia_view', id=complaint_id))

