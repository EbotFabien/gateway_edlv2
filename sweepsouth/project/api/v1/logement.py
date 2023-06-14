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
            '''URL="http://195.15.228.250/security/manager_app/viewset/role/"
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
            
            URL="http://195.15.228.250/logement/cles/tous"
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
@logement.route('/single/clefs/')
class clefsin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/cles/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
            URL="http://195.15.228.250/logement/cles/ajouter"
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
            URL="http://195.15.228.250/logement/cles/update/"+req_data['id']
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
@logement.route('/single/compteurs/')
class compteursin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/compteurs/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400


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
            URL="http://195.15.228.250/logement/compteur/ajouter"
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
            
            URL="http://195.15.228.250/logement/compteur/tous"
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
            URL="http://195.15.228.250/logement/compteur/update/"+req_data['id']
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



#client route
@logement.doc(
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
@logement.route('/single/client/')
class clientin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/client/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
@logement.route('/logement/client/add')
class clientadd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/client/ajouter"
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
@logement.route('/logement/client/all')
class clienta(Resource):
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
            
            URL="http://195.15.228.250/logement/client/tous"
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
@logement.route('/logement/client/modify')
class clientmod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/client/update/"+req_data['id']
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



#extension

@logement.doc(
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
@logement.route('/single/extension/')
class extensionin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/extenssion/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
@logement.route('/logement/extension/add')
class extensionadd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/extension/ajouter"
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
@logement.route('/logement/extension/all')
class extensiona(Resource):
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
            
            URL="http://195.15.228.250/logement/extenssion/tous"
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
@logement.route('/logement/extension/modify')
class extensionmod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/extenssion/update/"+req_data['id']
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


#piece

@logement.doc(
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
@logement.route('/single/piece/')
class piecein(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/piece/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
@logement.route('/logement/piece/add')
class pieceadd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/piece/ajouter"
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
@logement.route('/logement/piece/all')
class piecea(Resource):
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
            
            URL="http://195.15.228.250/logement/piece/tous"
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
@logement.route('/logement/piece/modify')
class piecemod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/piece/update/"+req_data['id']
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

#rubrique

@logement.doc(
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
@logement.route('/single/rubriq/')
class rubriqin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/rubriq/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
@logement.route('/logement/rubriq/add')
class rubriqadd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/rubriq/ajouter"
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
@logement.route('/logement/rubriq/all')
class rubriqa(Resource):
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
            
            URL="http://195.15.228.250/logement/rubriq/tous"
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
@logement.route('/logement/rubriq/modify')
class rubriqmod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/rubriq/update/"+req_data['id']
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


#type logement
@logement.doc(
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
@logement.route('/single/type_log/')
class type_login(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/type_log/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
@logement.route('/logement/type_log/add')
class type_logadd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/type_log/ajouter"
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
@logement.route('/logement/type_log/all')
class type_loga(Resource):
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
            
            URL="http://195.15.228.250/logement/type_log/tous"
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
@logement.route('/logement/type_log/modify')
class type_logmod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/type_log/update/"+req_data['id']
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



#voie

@logement.doc(
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
@logement.route('/single/voie/')
class voiein(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/voie/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
@logement.route('/logement/voie/add')
class voieadd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/voie/ajouter"
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
@logement.route('/logement/voie/all')
class voiea(Resource):
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
            
            URL="http://195.15.228.250/logement/voie/tous"
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
@logement.route('/logement/voie/modify')
class voiemod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/voie/update/"+req_data['id']
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



#user
@logement.doc(
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
@logement.route('/single/user/')
class userin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/user/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
@logement.route('/logement/user/add')
class useradd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/user/ajouter"
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
@logement.route('/logement/user/all')
class usera(Resource):
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
            
            URL="http://195.15.228.250/logement/user/tous"
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
@logement.route('/logement/user/modify')
class usermod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/user/update/"+req_data['id']
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


#logement

@logement.doc(
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
@logement.route('/single/logement/')
class logementin(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.228.250/logement/logement/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
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
@logement.route('/logement/logement/add')
class logementadd(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/logement/ajouter"
            r = requests.post(url=URL,json=req_data)
            if r.status_code == 200 :
                v=r.json()
                
                
                url1="http://195.15.218.172/synchro/edl/logement/ajouter/"
                r2 = requests.post(url=url1,json=v)
                return {
                        'status': 1,
                        'synchro_status':r2.json(),
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
@logement.route('/logement/logement/all')
class logementa(Resource):
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
            
            URL="http://195.15.228.250/logement/logement/tous"
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
@logement.route('/logement/logement/modify')
class logementmod(Resource):
    @token_required
    @logement.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.228.250/logement/logement/update/"+req_data['id']
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
@logement.route('/logement/print/pdf')
class logementprint(Resource):
    @token_required
    @logement.expect(parti)
    def post(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/edluser/print/file"
            r = requests.post(url=URL,json=req_data)
            print(r)
            return r
            
        else:
                return {
                        'status':0,
                        'res': 'input token',
                    }, 403
