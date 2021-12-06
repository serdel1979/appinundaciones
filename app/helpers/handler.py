from flask import request, render_template
from flask.json import jsonify

def bad_request(e):
    kwargs = {
        "error_name": "400 Bad Request",
        "error_description": "Su requerimiento contiene errores.",
    }
    page = "page-400.html"
    return make_response(kwargs, 400, page)

def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe.",
    }
    page = "page-404.html"
    return make_response(kwargs, 404, page)

def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No esta autorizado para acceder a ese url.",
    }
    page = "page-401.html"
    return make_response(kwargs, 401, page)

def forbidden_error(e):
    kwargs = {
        "error_name": "403 Forbidden Error",
        "error_description": "No tiene autorizacion para acceder a ese url.",
    }
    page = "page-403.html"
    return make_response(kwargs, 403, page)

def server_error(e):
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": f'Error interno de servidor"',
    }
    page = "page-500.html" 
    return make_response(kwargs, 500, page)


def validation_error(status, message):
    kwargs = {
        "error_name": f'{status} Bad Request',
        "error_description": message,
    }
    return jsonify(kwargs), status

def general_error(status, message):
    kwargs = {
        "error_name": f'{status}',
        "error_description": f"{message['error']}"
    }
    return jsonify(kwargs), status

def make_response(data, status, page):
    if request.path.startswith('/api/'):
        return jsonify(data),status
    else:
        return render_template(page, **data), status