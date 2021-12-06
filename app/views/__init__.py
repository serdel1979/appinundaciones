# -*- encoding: utf-8 -*-

from flask import Blueprint


blueprint = Blueprint(
    'blueprint',
    __name__,
    url_prefix='',
    template_folder='../templates',
    static_folder='../static'
)



# solución simple al tema de colors. Se evitan sessiones y
# globales al ejecutarse lo siguiente antes de cada render:
@blueprint.app_context_processor
def inject_colors_to_all_templates():
    from app.models.config import Configuration
    return dict(colors=Configuration.get_private_app())
