from flask import render_template, url_for, send_from_directory

from . import APP

from . import api

from .db_models import STD_STRING_SIZE

if APP.config.get('DEBUG', False):
    from . import debug_routes
