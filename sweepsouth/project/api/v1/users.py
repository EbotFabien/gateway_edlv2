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
    "trigramme":fields.String(required=False,default=" ", description="Users trigramme"),
    "role":fields.String(required=False,default=" ", description="Users role"),
})



@users.doc(
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
            
            URL="http://195.15.218.172/agent_app/agent/"+str(user_data['id'])
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