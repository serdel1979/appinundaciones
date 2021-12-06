from functools import wraps
from flask import render_template
from flask_login import current_user
from flask.globals import session


def user_has(permission, user=current_user):
    """
    Takes a string name of a permission and returns the function if the user has that permission
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            from app.models import Permission
            desired_permission = Permission.query.filter_by(
                name=permission).first()
            # user_permissions=user.get_permissions()
            user_permissions = session["permisos"]
            if desired_permission and desired_permission.name in user_permissions:
                return func(*args, **kwargs)
            else:
                return render_template('page-403.html')
        return inner
    return wrapper


def user_is(role, user=current_user):
    """
    Takes a string name of a role and returns the function if the user has that role
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if role in user.roles:
                return func(*args, **kwargs)
            return render_template('page-403.html')
        return inner
    return wrapper


def google_user_prohibited(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = current_user
        if user.is_google_user():
            return render_template('page-403.html')
        else:
            return func(*args, **kwargs)
    return wrapper