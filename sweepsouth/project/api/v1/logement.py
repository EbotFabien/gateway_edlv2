from flask_restx import Namespace, Resource, fields,marshal,Api
import jwt, uuid, os
from flask_cors import CORS
from functools import wraps 
from flask import abort, request, session,Blueprint
from datetime import datetime
from flask import current_app as app
#from sqlalchemy import or_, and_, distinct, func
#from project import  cache  #, logging
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
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            '''URL="http://195.15.218.172/security/manager_app/viewset/role/"
            params ={"token":token}
            r = requests.post(url=URL,params=params)
            print(r)'''
        if not token:
            return {'message': 'Token is missing or not found.'}, 401
        if token :
            pass
        return f(*args, **kwargs)
    return decorated

api = Blueprint('api',__name__, template_folder='../templates')
logement1=Api( app=api, doc='/docs',version='1.4',title='AMSV2',\
description='', authorizations=authorizations)
#implement cors

CORS(api, resources={r"/api/*": {"origins": "*"}})

logement  = logement1.namespace('/api/logement', \
    description= "All routes under this section of the documentation are the open routes bots can perform CRUD action \
    on the application.", \
    path = '/v1/')


parti= logement.model('logement', {
    "nom": fields.String(required=False,default=" ", description="Users nom"),
})


#clefs route
@logement.doc(
    security='KEY',
    params={'start': 'Value to start from ',
             'limit': 'Total limit of the query',
             'count': 'Number results per page',
            'category': 'category'
            },
    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@logement.route('/logement/clefs/all')
class clefa(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/post/tags?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/post/tags?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/logement/cles/tous"
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "start": start,
                    "limit": limit,
                    "count": count,
                    "next": next,
                    "previous": previous,
                    "results": r.json()
                }, 200
            else:
                return{
                    "res":"Clefs logement service down"
                }, 400

@logement.doc(
    security='KEY',
    params={},

    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@logement.route('/logement/clefs/add')
class clefsadd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/logement/cles/ajouter"
            r = requests.post(url=URL,json=req_data)
            if r.status_code == 200 :
                return {
                        'status': 1,
                        'res': r.json(),
                    }, 200
            else:
                return {
                        'status':0,
                        'res': 'failed',
                    }, 400
        else:
                return {
                        'status':0,
                        'res': 'input token',
                    }, 403

@logement.doc(
    security='KEY',
    params={},

    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@logement.route('/logement/clefs/modify')
class clefsmod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/logement/logement/cles/update/"+req_data['id']
            r = requests.post(url=URL,json=req_data)
            if r.status_code == 200 :
                return {
                        'status': 1,
                        'res': r.json(),
                    }, 200
            else:
                return {
                        'status':0,
                        'res': 'failed',
                    }, 400
        else:
                return {
                        'status':0,
                        'res': 'input token',
                    }, 403


#compteurs route
@logement.doc(
    security='KEY',
    params={},

    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@logement.route('/logement/compteurs/add')
class compteuradd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/logement/logement/compteur/ajouter"
            r = requests.post(url=URL,json=req_data)
            if r.status_code == 200 :
                return {
                        'status': 1,
                            'res': r.json(),
                    }, 200
            else:
                return {
                        'status':0,
                        'res': 'failed',
                    }, 400
        else:
                return {
                        'status':0,
                        'res': 'input token',
                    }, 403


@logement.doc(
    security='KEY',
    params={'start': 'Value to start from ',
             'limit': 'Total limit of the query',
             'count': 'Number results per page',
            'category': 'category'
            },
    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@logement.route('/logement/compteurs/all')
class compteursa(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/post/tags?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/post/tags?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/logement/logement/compteur/tous"
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "start": start,
                    "limit": limit,
                    "count": count,
                    "next": next,
                    "previous": previous,
                    "results": r.json()
                }, 200
            else:
                return{
                    "res":"compteurs logement service down"
                }, 400


@logement.doc(
    security='KEY',
    params={},

    responses={
        200: 'ok',
        201: 'created',
        204: 'No Content',
        301: 'Resource was moved',
        304: 'Resource was not Modified',
        400: 'Bad Request to server',
        401: 'Unauthorized request from client to server',
        403: 'Forbidden request from client to server',
        404: 'Resource Not found',
        500: 'internal server error, please contact admin and report issue'
    })
@logement.route('/logement/compteurs/modify')
class compteursmod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/logement/compteur/update/"+req_data['id']
            r = requests.post(url=URL,json=req_data)
            if r.status_code == 200 :
                return {
                        'status': 1,
                        'res': r.json(),
                    }, 200
            else:
                return {
                        'status':0,
                        'res': 'failed',
                    }, 400
        else:
                return {
                        'status':0,
                        'res': 'input token',
                    }, 403


