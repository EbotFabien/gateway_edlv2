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

# The token decorator to protect my routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                data =token
            except:
                return {'message': 'Token is invalid.'}, 403
        if not token:
            return {'message': 'Token is missing or not found.'}, 401
        if data:
            pass
        return f(*args, **kwargs)
    return decorated

api = Blueprint('api',__name__, template_folder='../templates')
users1=Api( app=api, doc='/docs',version='1.4',title='AMS V2A',\
description='', authorizations=authorizations)
#implement cors

CORS(api, resources={r"/api/*": {"origins": "*"}})

users  = users1.namespace('/api/utilisateurs', \
    description= "All routes under this section of the documentation are the open routes bots can perform CRUD action \
    on the application.", \
    path = '/v1/')


users2= users.model('users', {
    "id": fields.Integer(required=True),
    "nom": fields.String(required=False,default=" ", description="Users nom"),
    "prenom":fields.String(required=False,default=" ", description="Users prenom"),
    "email":fields.String(required=False,default=" ", description="Users Email"),
    "mdp":fields.String(required=False,default=" ", description="Users mdp"),
    "adresse":fields.String(required=False,default=" ", description="Users adresse"),
    "telephone":fields.String(required=False,default=" ", description="Users trigramme"),
})
 



@users.doc(
    security='KEY',
    params={'start': 'Value to start from ',
             'limit': 'Total limit of the query',
             'count': 'Number results per page'
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
@users.route('/users/all')
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
            
            URL="http://195.15.218.172/edluser/Agentsec/tous"
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

@users.doc(
    security='KEY',
    params={'start': 'Value to start from ',
             'limit': 'Total limit of the query',
             'count': 'Number results per page'
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
@users.route('/users/all')
class usera(Resource):
    def get(self):
        if request.args:
            start = request.args.get('start', None)
            limit = request.args.get('limit', None)
            count = request.args.get('count', None)
            # Still to fix the next and previous WRT Sqlalchemy
            next = "/api/v1/users/all?start=" + \
                str(int(start)+1)+"&limit="+limit+"&count="+count
            previous = "/api/v1/users/all?start=" + \
                str(int(start)-1)+"&limit="+limit+"&count="+count
            
            URL="http://195.15.218.172/edluser/Agentsec/tous"
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


@users.doc(
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
@users.route('/single/user/')
class userp(Resource):
    def get(self):
        if request.args:
            start = request.args.get('ID', None)
            URL="http://195.15.218.172/edluser/Agentsec/"+start
            r = requests.get(url=URL)
            if r.status_code == 200:
                return {
                    "results":r.json()
                }, 200
            else:
                return{
                    "res":"User service down"
                }, 400


@users.doc(
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
@users.route('/update/users')
class Update(Resource):
    @token_required
    @users.expect(users2)
    def put(self):
        user_data = request.get_json()
        token = request.headers['Authorization']
        if token:
            
            #URL="http://195.15.218.172/edluser/Agentsec/"+str(user_data['id'])
            URL="http://195.15.228.250/admin_app/admin/"+str(user_data['id'])
            headers ={"Authorization":token}
            #for key,value in user_data.iteritems():
            #    if value == None:
            #        del user_data[key]
            del user_data['id']
            

            r = requests.put(url=URL,headers=headers,json=user_data)

            if r.status_code == 200 :
                v=r.json()
                try:
                    if user_data["mdp"] != "":
                        v[0]['mdp']=user_data["mdp"]
                except:
                    pass
                url1="http://195.15.218.172/synchro/util/edit/"
                r2 = requests.post(url=url1,json=v)
                return {
                        'status': 1,
                        'synchro_status':r2.status_code,
                        'res': r.json(),
                    }, 200
                
            else:
                return {
                        'status':r.status_code,
                        'res': 'failed',
                    }, 400
               
                
        else:
                return {
                        'status':0,
                        'res': 'no data',
                    }, 401
