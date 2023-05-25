from flask_restx import Namespace, Resource, fields,marshal,Api
import jwt, uuid, os
from flask_cors import CORS
from functools import wraps 
from flask import abort, request, session,Blueprint
from datetime import datetime
from flask import current_app as app
#from sqlalchemy import or_, and_, distinct, func
#from project import cache   #, logging
import requests



authorizations = {
    'KEY': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
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
biblio1=Api( app=api, doc='/docs',version='1.4',title='AMS.',\
description='', authorizations=authorizations)
#implement cors

CORS(api, resources={r"/api/*": {"origins": "*"}})

biblio  = biblio1.namespace('/api/biblio', \
    description= "All routes under this section of the documentation are the open routes bots can perform CRUD action \
    on the application.", \
    path = '/v1/')


client= biblio.model('client', {
    "nom": fields.String(required=False,default=" ", description="Users nom")
})


@biblio.doc(
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
@biblio.route('/clefs/all')
class clefa(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/clefs/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/clefs/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/Clefs/tous"
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
                    "res":"Clefs biblio service down"
                }, 400

@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/clefs/')
class clefsi(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/Clefs/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400

@biblio.doc(
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
@biblio.route('/clefs/add')
class clefsadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/Clefs/ajouter"
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

@biblio.doc(
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
@biblio.route('/clefs/modify')
class clefsmod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/Clefs/update/"+req_data['id']
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


@biblio.doc(
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
@biblio.route('/commentaire/all')
class commentairea(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/commentaire/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/commentaire/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/commentaire/tous"
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
                    "res":"Commentaire biblio service down"
                }, 400

@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/commentaire/')
class commentairesin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/commentaire/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400

@biblio.doc(
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
@biblio.route('/commentaire/add')
class commentadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/commentaire/ajouter"
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

@biblio.doc(
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
@biblio.route('/commentaire/modify')
class commentairemod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/commentaire/update/"+req_data['id']
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


@biblio.doc(
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
@biblio.route('/compteurs/add')
class compteuradd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/compteurs/ajouter"
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


@biblio.doc(
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
@biblio.route('/compteurs/all')
class compteursa(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/compteurs/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/compteurs/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/compteurs/tous"
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
                    "res":"compteurs biblio service down"
                }, 400

@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/compteurs/')
class compteursin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/compteurs/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400


@biblio.doc(
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
@biblio.route('/compteurs/modify')
class compteursmod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/compteurs/update/"+req_data['id']
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

@biblio.doc(
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
@biblio.route('/extension/add')
class extensionadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/extension/ajouter"
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


@biblio.doc(
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
@biblio.route('/extension/all')
class extensiona(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/extension/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/extension/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/extension/tous"
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
                    "res":"extensions biblio service down"
                }, 400

@biblio.doc(
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
@biblio.route('/extension/modify')
class extensionmod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/extension/update/"+req_data['id']
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

@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/extension/')
class extensions(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/extension/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400


@biblio.doc(
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
@biblio.route('/logement/add')
class logementadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/logement/ajouter"
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


@biblio.doc(
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
@biblio.route('/logement/all')
class logementa(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/logement/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/logement/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/logement/tous"
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
                    "res":"logement biblio service down"
                }, 400
            
@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/logement/')
class logemensin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/logement/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400


@biblio.doc(
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
@biblio.route('/logement/modify')
class logementmod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/logement/update/"+req_data['id']
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
        

@biblio.doc(
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
@biblio.route('/piece/add')
class pieceadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/piece/ajouter"
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

@biblio.doc(
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
@biblio.route('/piece/all')
class piecea(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/piece/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/piece/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/piece/tous"
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
                    "res":"piece biblio service down"
                }, 400

@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/piece/')
class piecesin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/piece/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400


@biblio.doc(
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
@biblio.route('/piece/modify')
class piecemod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/piece/update/"+req_data['id']
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

@biblio.doc(
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
@biblio.route('/rubric/add')
class rubricadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/Rubric/ajouter"
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


@biblio.doc(
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
@biblio.route('/rubric/all')
class rubrica(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/rubric/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/rubric/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/Rubric/tous"
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
                    "res":"rubric biblio service down"
                }, 400

@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/rubric/')
class rubricsin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/Rubric/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400

@biblio.doc(
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
@biblio.route('/Rubric/modify')
class Rubricmod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/Rubric/update/"+req_data['id']
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

@biblio.doc(
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
@biblio.route('/typecom/add')
class typecomadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/typecom/ajouter"
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

@biblio.doc(
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
@biblio.route('/typecom/all')
class typecoma(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/typecom/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/typecom/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/typecom/tous"
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
                    "res":"typecom biblio service down"
                }, 400


@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/typecom/')
class typecomsin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/typecom/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400

@biblio.doc(
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
@biblio.route('/typecom/modify')
class typecommod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/typecom/update/"+req_data['id']
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

@biblio.doc(
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
@biblio.route('/typeloge/add')
class typelogeadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/typeloge/ajouter"
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

@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/typeloge/')
class typelogesin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/typeloge/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400


@biblio.doc(
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
@biblio.route('/typeloge/all')
class typelogea(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/typeloge/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/typeloge/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/typeloge/tous"
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
                    "res":"typeloge biblio service down"
                }, 400

@biblio.doc(
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
@biblio.route('/typeloge/modify')
class typelogemod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/typeloge/update/"+req_data['id']
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

@biblio.doc(
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
@biblio.route('/voie/add')
class voieadd(Resource):
    @token_required
    @biblio.expect(client)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/voie/ajouter"
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


@biblio.doc(
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
@biblio.route('/voie/all')
class voiea(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/voie/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/voie/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/biblio/voie/tous"
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
                    "res":"voie biblio service down"
                }, 400

@biblio.doc(
    security='KEY',
    params={'ID': 'Identity of User'
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
@biblio.route('/single/voie/')
class voiesin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/biblio/voie/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400

@biblio.doc(
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
@biblio.route('/voie/modify')
class voiemod(Resource):
    @token_required
    @biblio.expect(client)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/biblio/voie/update/"+req_data['id']
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