from flask_restx import Namespace, Resource, fields,marshal,Api
import jwt, uuid, os
from flask_cors import CORS
from functools import wraps 
from flask import abort, request, session,Blueprint
from datetime import datetime
from flask import current_app as app
#from sqlalchemy import or_, and_, distinct, func
#from project import cache  #, logging
import requests




authorizations = {
    'KEY': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'API-KEY'
    }
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'API-KEY' in request.headers:
            token = request.headers['API-KEY']
            try:
                data = jwt.decode(token, app.config.get('SECRET_KEY'))
            except:
                return {'message': 'Token is invalid.'}, 403
        if not token:
            return {'message': 'Token is missing or not found.'}, 401
        if data:
            pass
        return f(*args, **kwargs)
    return decorated

api = Blueprint('api',__name__, template_folder='../templates')
rdv1=Api( app=api, doc='/docs',version='1.4',title='AMS',\
description='', authorizations=authorizations)
#implement cors

CORS(api, resources={r"/api/*": {"origins": "*"}})

rdv  = rdv1.namespace('/api/rdv', \
    description= "All routes under this section of the documentation are the open routes bots can perform CRUD action \
    on the application.", \
    path = '/v1/')
