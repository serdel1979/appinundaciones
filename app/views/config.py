from flask import render_template, redirect, url_for, flash, request
from app.views import blueprint
from app.forms import ConfigurationForm
from app.models import Configuration
from flask_login import login_required
from app.helpers.decorators import user_has



@blueprint.route('/configuration', methods=['GET','POST'])
@login_required
@user_has('configuracion_app_update')
def edit_config():
    conf = Configuration.current()
    form = ConfigurationForm(obj=conf)
    if form.is_submitted():
        default = request.form.get("default")
        if default: 
            conf.update( num_elems = 5, order_by = 0,
            public_first        = "#B744B8",
            public_second       = "#B744B8",
            public_third        = "#ededed",
            private_first       = "#B744B8",
            private_second      = "#B744B8",
            private_third       = "#ededed",
            )
        if default is None:
            n = request.form["num_elems"]
            if int(n) <= 0 or int(n) > 100:
                flash("Por favor, ingrese un numero de elementos valido entre 1 y 100", "error")
                return redirect(url_for('blueprint.edit_config'))
            if form.validate():
                conf.update(num_elems           = request.form["num_elems"],
                            order_by            = request.form["order_by"],
                            public_first        = request.form["public_primary_color_hex"],
                            public_second       = request.form["public_secondary_color_hex"],
                            public_third        = request.form["public_terciary_color_hex"],
                            private_first       = request.form["private_primary_color_hex"],
                            private_second      = request.form["private_secondary_color_hex"],
                            private_third       = request.form["private_terciary_color_hex"]
                            )
                conf.save_edit()
        flash("cambios registrados con éxito", "success")
        return redirect(url_for('blueprint.edit_config'))
    return render_template('config.html', form=form)
