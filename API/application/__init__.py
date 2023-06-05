import sys 
# setting path
# sys.path.append('../main.py')
from flask import Flask
from .models import db
from .resources import api
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from .utils.error import generic_error_handler, http_exception_handler
from .utils.security import user_datastore, sec
from .utils.stop_cookie import CustomSessionInterface
from .utils.extra_endpoin_urls import all_post_short, user_info_short, remove_post_image, all_user_info_short, all_user_info_short_follow,export_posts
from .cache import cache
# from .celery_system import make_celery
# from main import celery
import random, time

# celery = make_celery()
# global celery


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.update (
        CELERY_BROKER_URL = 'redis://localhost:6379/2',
        CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'
    )
    app.session_interface = CustomSessionInterface()
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    sec.init_app(app, user_datastore)
    # celery = make_celery(app)
    # celery.init_app(app)
    cache.init_app(app)
    app.register_error_handler(Exception, generic_error_handler)
    app.register_error_handler(HTTPException, http_exception_handler)
    app.add_url_rule('/api/extra/all_post_short/<int:filter_id>', 'all_post_short', all_post_short)
    app.add_url_rule('/api/extra/user_info_short/<int:user_id>', 'user_info_short', user_info_short)
    app.add_url_rule('/api/extra/remove_post_image/<int:id>', 'remove_post_image', remove_post_image)
    app.add_url_rule('/api/extra/all_user_info_short', 'all_user_info_short', all_user_info_short)
    app.add_url_rule('/api/extra/all_user_info_short_follow/<string:list>/<int:id>', 'all_user_info_short_follow', all_user_info_short_follow)
    app.add_url_rule('/api/extra/export_posts', 'export_posts', export_posts)
    export_posts
    return app

