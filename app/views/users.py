# -*- encoding: utf-8 -*-

import datetime
from flask.globals import session
from flask_login import current_user, login_user, logout_user
from email_validator import validate_email, EmailNotValidError
from flask_login.utils import login_required
from flask.helpers import flash
from app.forms import CreateResetPasswordForm, CreateSearchForm
from app.views import blueprint
from flask import render_template, redirect, url_for, request
from app.forms import LoginForm, RolesForm, CreateAccountForm
from app.models import User, Role, Configuration, UserPending
from app.helpers.util import verify_pass, hash_pass
from app.helpers.decorators import user_has, google_user_prohibited
from app import client, app_config, GOOGLE_DISCOVERY_URL
import requests
import json


## Login & Registration


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@blueprint.route("/google-login")
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.url_root + "login/callback",
        scope=["email", "profile"],
    )
    return redirect(request_uri)


@blueprint.route("/google-signup")
def google_signup():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.url_root + "signup/callback",
        scope=["email", "profile"],
    )
    return redirect(request_uri)


def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app_config.GOOGLE_CLIENT_ID, app_config.GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens, let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        return userinfo_response.json()
    else:
        return "User email not available or not verified by Google.", 400


@blueprint.route("/login/callback")
def login_callback():
    user_json = callback()
    email = user_json["email"]
    user = User.get_by_email(email)
    if user:
        if not user.active:
            flash("Usuario inactivo", "error")
            return render_template('accounts/login.html')
        # antes de logearnos, actualizamos su nombre y apellido, ya
        # que el usuario pudo haberlos modificado desde google
        user.first_name = user_json.get('given_name', None)
        user.last_name = user_json.get('family_name', None)
        user.save()
        login_user(user)
        load_permissions(user)
    elif UserPending.get_by_email(email):
        flash("La solicitud de registro sigue pendiente de aceptación", 'warning')
    else:
        flash("La cuenta de google no corresponde a un usuario registrado", "warning")
    return redirect(url_for('blueprint.route_default'))


@blueprint.route("/signup/callback")
def signup_callback():
    user_json = callback()
    email = user_json["email"]
    username = email
    if User.get_by_username(username):
        flash("Ya estás registrado", 'warning')
    elif User.get_by_email(email):
        flash("El email ya se encuentra registrado", 'error')
    elif UserPending.get_by_email(email):
        flash("Existe una solicitud pendiente de aceptación", 'error')
    else:  # creamos la solicitud de registro pendiente
        first_name = user_json.get('given_name', None)
        last_name = user_json.get('family_name', None)
        pending = UserPending(username, first_name, last_name, email)
        pending.save()
        flash("Ya se envió la solicitud, un administrador la evaluará.", 'success')
    return redirect(url_for('blueprint.route_default'))


@blueprint.route('/pending_list', methods=['POST', 'GET'])
@login_required
@user_has('solicitud_index')
def pending_list():
    form = RolesForm()
    form.roles.choices = [(c.id, c.name)
                          for c in Role.query.order_by(Role.name).all()]
    per_page = Configuration.get_num_elems()
    order_by = 'email asc' if Configuration.is_ascendent() else 'email desc'
    # del campo hidden del template
    page = request.form.get('page')
    current_page = int(page) if page else 1
    search_email = request.form.get('search')
    if search_email:
        pendings = UserPending.search_pending(search_email, order_by).paginate(
            current_page, per_page, error_out=False)
    else:
        pendings = UserPending.all_pendings(order_by).paginate(
            current_page, per_page, error_out=False)
    if not len(pendings.items) and search_email:
        flash("No hubo coincidencias en su búsqueda", "warning")

    return render_template("accounts/pending-list.html", pendings=pendings, form=form)


@blueprint.route('/pending-accept', methods=['POST'])
@login_required
@user_has('usuario_new')
def pending_accept():
    pending = UserPending.get_by_id(request.form.get('pendingToAccept'))
    role_ids = request.form.getlist('roles')
    if not role_ids:
        flash("Seleccione al menos un rol", 'error')
    else:
        user = User(username=pending.username, first_name=pending.first_name,
                    last_name=pending.last_name, email=pending.email, roles=role_ids)
        user.save()
        UserPending.delete(pending.id)
        flash("Usuario registrado exitosamente", 'success')
    return redirect(url_for('blueprint.pending_list'))


@blueprint.route('/pending-reject', methods=['POST'])
@login_required
@user_has('usuario_new')
def pending_reject():
    UserPending.delete(request.form.get('pendingToReject'))
    flash("Solicitud rechazada", 'success')
    return redirect(url_for('blueprint.pending_list'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        # read form data
        username = request.form['username']
        password = request.form['password']

        user = User.get_by_username(username)
        # Check the password
        if user and verify_pass(password, user.password):
            if not user.active:
                flash("Usuario inactivo", "error")
                return render_template('accounts/login.html', form=login_form)
            login_user(user)
            # carga los permisos del usuario en la sesion
            load_permissions(user)
            return redirect(url_for('blueprint.route_default'))
        logout_user()
        flash("Usuario o clave incorrecto", "error")
        return render_template('accounts/login.html', form=login_form)
    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    return redirect(url_for('blueprint.index'))


def load_permissions(user):
    """
    Cuando se puede hacer login, se cargan los datos del usuario en 
    la sesión
    """
    session["id"] = user.id
    session["username"] = user.username
    session["permisos"] = user.get_permissions()


@blueprint.route('/register', methods=['GET', 'POST'])
@login_required
@user_has('usuario_new')
def register():
    form = CreateAccountForm(request.form)
    form.roles.choices = [(c.id, c.name)
                          for c in Role.query.order_by(Role.name).all()]
    if 'register' in request.form:
        email = request.form['email']
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            print(str(e))
            flash("El email ingresado no es válido", 'error')
            return render_template('accounts/register.html', form=form)
        username = request.form['username']
        try:
            validate_email(username)
        except EmailNotValidError:
            pass
        else:
            # el username no puede ser un email, resolución efectiva
            # ante posibles dolores de cabeza (en registro con google
            # establecemos que username es igual a email)
            flash("El nombre de usuario no puede ser un email", 'error')
            flash("Solo permitido a usuarios registrados por Google", 'error')
            return render_template('accounts/register.html', form=form)
        if request.form['password'] != request.form['retry_password']:
            flash("Las contraseñas no coinciden", 'error')
        elif User.get_by_username(username):
            flash("El nombre de usuario ya se encuentra registrado", 'error')
        elif User.get_by_email(email):
            flash("El email ya se encuentra registrado", 'error')
        elif UserPending.get_by_email(email):
            flash("El email pertenece a un usuario pendiente de aprobación", 'error')
        elif not request.form.getlist('roles'):
            flash("Seleccione al menos un rol", 'error')
        else:  # Se puede crear el usuario
            user = User(request.form['username'], request.form['first_name'], request.form['last_name'],
                        request.form['email'], request.form['password'], request.form.getlist('roles'))
            user.save()
            flash("Usuario registrado exitosamente", 'success')
            return redirect(url_for("blueprint.register"))
        return render_template('accounts/register.html', form=form)
    else:
        return render_template('accounts/register.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('blueprint.login'))


@blueprint.route('/user_list', methods=['POST', 'GET'])
@login_required
def user_list():
    """
    Ruta que muestra el listado de usuarios del sistema
    """
    form = CreateSearchForm(request.form)
    per_page = Configuration.get_num_elems()
    page = request.form.get('page')  # del campo hidden del template
    current_page = int(page) if page else 1
    username = request.form.get('search')
    active = bool(request.form.get('active'))
    order_by = 'username asc' if Configuration.is_ascendent() else 'username desc'
    if not username:
        encontrados = User.all(not active, order_by).paginate(
            current_page, per_page, error_out=False)
    else:
        encontrados = User.by_username(username, not active, order_by).paginate(
            current_page, per_page, error_out=False)
    return render_template("accounts/user-list.html", users=encontrados, form=form)


@blueprint.route('/users/<int:id>/toggle-status')
@login_required
@user_has('usuario_change_status')
def delete_user(id):
    user = User.get_by_id(id)
    if not user:
        flash("Usuario inexistente", "error")
    elif 'administrador' in user.roles:
        flash("No se puede bloquear a un administrador", "error")
    else:
        user.toggle()
        if user.active:
            flash("Usuario activado exitosamente", "success")
        else:
            flash("Usuario bloqueado exitosamente", "success")
    return redirect(url_for("blueprint.user_list"))


@blueprint.route('/users/<int:id>/view', methods=['GET'])
@login_required
def user_view(id):
    user = User.get_by_id(id)
    return render_template('accounts/user-show.html', user=user)


@blueprint.route('/current-user/profile', methods=['GET'])
@login_required
def user_profile():
    return render_template('accounts/user-profile.html', user=current_user)


@blueprint.route('/current-user/edit-profile', methods=['GET'])
@login_required
@google_user_prohibited
def edit_profile():
    return render_template('accounts/edit-my-profile.html', user=current_user)


@blueprint.route('/current-user/update-profile/', methods=['POST'])
@login_required
@google_user_prohibited
def update_profile():
    user = User.get_by_email(email=request.form.get('email'))
    if (user) and (user.id != current_user.id):
        flash("El email ya se encuentra registrado", 'error')
        return redirect(url_for("blueprint.edit_profile", id=id))
    current_user.email = request.form.get("email")
    current_user.updated_at = datetime.datetime.now()
    current_user.first_name = request.form.get("first_name")
    current_user.last_name = request.form.get("last_name")
    current_user.save()
    flash("Perfil actualizado exitosamente", 'success')
    return render_template('accounts/user-profile.html', user=current_user)


@blueprint.route('/users/<int:id>/edit', methods=['GET'])
@login_required
@user_has('usuario_update')  # este permiso permite modificar OTROS usuarios
def edit_another_user(id):
    user = User.get_by_id(id)
    roles = Role.all()
    return render_template('accounts/user-edit.html', user=user, roles=roles)


@blueprint.route('/users/<int:id>', methods=['POST'])
@login_required
@user_has('usuario_update')
def user_update(id):
    another_user = User.get_by_username(request.form.get('username'))
    if another_user and (another_user.id != id):
        flash("El nombre de usuario ya se encuentra registrado", 'error')
        return redirect(url_for("blueprint.edit_another_user", id=id))
    another_user = User.get_by_email(request.form.get('email'))
    if another_user and (another_user.id != id):
        flash("El email ya se encuentra registrado", 'error')
        return redirect(url_for("blueprint.edit_another_user", id=id))
    user = User.get_by_id(id)
    already_admin = user.is_admin()
    user.email = request.form.get("email")
    user.username = request.form.get("username")
    user.updated_at = datetime.datetime.now()
    user.first_name = request.form.get("first_name")
    user.last_name = request.form.get("last_name")
    user.roles.clear()
    user.add_roles(request.form.getlist('roles'))
    if 'administrador' in user.roles:
        user.active = True  # siempre estará activo
    else:
        value = request.form.get("active")
        user.active = bool(value)
        if already_admin:  # era admin y le quieren sacar ese rol
            user.add_existing_role_by_name('administrador')
            user.active = True
            user.save()
            flash("no se puede quitar el rol de administrador", "error")
            return redirect(url_for("blueprint.user_list"))
    user.save()
    flash("El usuario se ha actualizado exitosamente", 'success')
    return redirect(url_for("blueprint.user_list"))


@blueprint.route('/google-users/<int:id>/edit', methods=['GET'])
@login_required
@user_has('usuario_update')  # este permiso permite modificar OTROS usuarios
def edit_google_user(id):
    user = User.get_by_id(id)
    roles = Role.all()
    return render_template('accounts/user-edit.html', user=user, roles=roles)




@blueprint.route('/reset-password', methods=['GET'])
@login_required
@google_user_prohibited
def reset_password():
    form = CreateResetPasswordForm(request.form)
    return render_template("accounts/reset-password.html", form=form)


@blueprint.route('/change-password', methods=['POST'])
@login_required
@google_user_prohibited
def change_password():
    login_form = LoginForm(request.form)
    create_reset_password_form = CreateResetPasswordForm(request.form)
    current_password = request.form['current_password']
    user = User.get_by_username(session.get("username"))
    # Check the password
    if not verify_pass(current_password, user.password):
        flash("La contraseña actual es incorrecta", 'error')
        return render_template('accounts/reset-password.html', form=create_reset_password_form)
    if request.form['password'] != request.form['retry_password']:
        flash("Las nuevas contraseñas no coinciden", 'error')
        return render_template('accounts/reset-password.html', form=create_reset_password_form)
    user.password = hash_pass(request.form['password'])
    user.save()
    logout_user()
    flash("Contraseña actualizada, vuelva a iniciar sesión", 'success')
    return render_template('accounts/login.html', form=login_form)
