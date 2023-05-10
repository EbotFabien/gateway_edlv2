from flask_restx import Namespace, Resource, fields,marshal,Api
import jwt, uuid, os
from functools import wraps 
from flask import abort,request,session,Blueprint
from datetime import datetime
from flask import current_app as app    
from flask_cors import CORS
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
planif1=Api( app=api, doc='/docs',version='1.4',title='Sweep API.',\
description='', authorizations=authorizations)
#implement cors
CORS(api, resources={r"/api/*": {"origins": "*"}})


planif  = planif1.namespace('/api/planif', \
    description= "All routes under this section of the documentation are the open routes bots can perform CRUD action \
    on the application.", \
    path = '/v1/')


parti= planif.model('participant', {
    "nom": fields.String(required=False,default=" ", description="Users nom"),
})


@planif.doc(
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
@planif.route('planif/participant/all')
class planifparticipant(Resource):
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
            
            URL="http://195.15.218.172/edluser/Admin/tous"
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
                    "res":"planif participant service down"
                }, 400


@planif.doc(
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
@planif.route('planif/users/all')
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
            
            URL="http://195.15.218.172/edluser/Admin/tous"
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "start": start,
                    "limit": limit,
                    "count": count,
                    "next": next,
                    "previous": previous,
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400

#edl routes
@planif.doc(
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
@planif.route('/planif/edl/all')
class edlall(Resource):
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
            
            URL="http://195.15.218.172/edluser/edl/tous"
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "start": start,
                    "limit": limit,
                    "count": count,
                    "next": next,
                    "previous": previous,
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"Planif edl service down"
                }, 400

@planif.doc(
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
@planif.route('/planif/edl/add')
class edl_add(Resource):
    @token_required
    @planif.expect(parti)
    def post(self):
        req_data = request.get_json()
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/participant/edl/ajouter"
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

@planif.doc(
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
@planif.route('/planif/edl/update')
class edl_update(Resource):
    @token_required
    @planif.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/participant/edl/modifier/"+req_data['id']
            del req_data['id']
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

@planif.doc(
    security='KEY',
    params={'start': 'Value to start from ',
             'limit': 'Total limit of the query',
             'count': 'Number results per page',
            'id': 'id'
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
@planif.route('/planif/edl/indivi')
class edlsing(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            ID = request.args.get('id', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/post/tags?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/post/tags?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/edluser/edl/"+ID
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "start": start,
                    "limit": limit,
                    "count": count,
                    "next": next,
                    "previous": previous,
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"Planif edl service down"
                }, 400


#users  route
@planif.doc(
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
@planif.route('/planif/users/all')
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
            
            URL="http://195.15.218.172/edluser/user/tous"
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "start": start,
                    "limit": limit,
                    "count": count,
                    "next": next,
                    "previous": previous,
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400

@planif.doc(
    security='KEY',
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
@planif.route('/planif/update/users')
class user_Update(Resource):
    @token_required
    @planif.expect(parti)
    def put(self):
        user_data = request.get_json()
        token = request.headers['Authorization']
        if token:
            
            URL="http://195.15.218.172/agent_app/user/update/"+str(user_data['id'])
            headers ={"Authorization":token}
            #for key,value in user_data.iteritems():
            #    if value == None:
            #        del user_data[key]

            del user_data['id']
            print(user_data)
            r = requests.post(url=URL,headers=headers,json=user_data)
            print(r.headers)
               
                
        else:
                return {
                        'status':0,
                        'res': 'no data',
                    }, 401


#participant route

@planif.doc(
    security='KEY',
    params={'start': 'Value to start from ',
             'limit': 'Total limit of the query',
             'count': 'Number results per page',
            
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
@planif.route('/planif/participant/all')
class planifparticipanta(Resource):
    @token_required
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
            
            URL="http://195.15.218.172/participant/participant/tous"
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
                    "res":"planif service down"
                }, 400



@planif.doc(
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
@planif.route('/planif/participant/add')
class planif_Parti_add(Resource):
    @token_required
    @planif.expect(parti)
    def post(self):
        req_data = request.get_json()
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/participant/participant/ajouter"
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


#rdv route
@planif.doc(
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
@planif.route('/planif/rdv/all')
class rdvall(Resource):
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
            
            URL="http://195.15.218.172/edluser/rdv/tous"
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "start": start,
                    "limit": limit,
                    "count": count,
                    "next": next,
                    "previous": previous,
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"Planif edl service down"
                }, 400

@planif.doc(
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
@planif.route('/planif/rdv/add')
class rdv_add(Resource):
    @token_required
    @planif.expect(parti)
    def post(self):
        req_data = request.get_json()
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/participant/rdv/ajouter"
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

@planif.doc(
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
@planif.route('/planif/rdv/update')
class rdv_update(Resource):
    @token_required
    @planif.expect(parti)
    def put(self):
        req_data = request.json
        
        token=request.headers['Authorization']
        if token:
            URL="http://195.15.218.172/participant/rdv/update/"+req_data['id']
            del req_data['id']
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

@planif.doc(
    security='KEY',
    params={'start': 'Value to start from ',
             'limit': 'Total limit of the query',
             'count': 'Number results per page',
            'id': 'id'
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
@planif.route('/planif/rdv/indivi')
class rdvsing(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            ID = request.args.get('id', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/post/tags?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/post/tags?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/edluser/rdv/"+ID
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "start": start,
                    "limit": limit,
                    "count": count,
                    "next": next,
                    "previous": previous,
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"Planif edl service down"
                }, 400

