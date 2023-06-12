from flask import Blueprint, url_for
from flask_restx import Api, Resource, fields, reqparse, marshal
from flask import Blueprint, render_template, abort, request, session
from flask_cors import CORS
from functools import wraps
import requests as rqs
#from tqdm import tqdm
from flask import current_app as app
from datetime import datetime, timedelta
#from project import db, limiter, cache,bcrypt
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import werkzeug
import json, shortuuid
import uuid
import jwt, uuid, os
from flask import current_app as app
#from sqlalchemy import func,or_,and_
import re
from .v1 import biblio,logement,participant,planif,rdv,users
import requests



# API security
authorizations = {
    'KEY': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
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

class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if '8055' in self.base_url else 'https'
        url=url_for(self.endpoint('specs'), _external=True)
        prefix=url.split('/swagger.json')[0]
        prefix=prefix.split('/api')[0]
        url=prefix +'/edlgateway'+'/swagger.json'
        return  url

    
api = Blueprint('api', __name__, template_folder = '../templates')
apisec = Api( app=api, doc='/docs', version='1.9.0', title='AMSV2A.', \
    description='This documentation contains all routes to access the AMSV2. \npip install googletransSome routes require authorization and can only be gotten \
    from the AMSV2A company', license='../LICENSE', license_url='www.sweep.com', contact='touchone0001@gmail.com', authorizations=authorizations)

CORS(api, resources={r"/api/*": {"origins": "*"}})

#from . import schema

apisec.add_namespace(biblio)
apisec.add_namespace(logement)
apisec.add_namespace(participant)
apisec.add_namespace(planif)
apisec.add_namespace(rdv)
apisec.add_namespace(users)


login = apisec.namespace('/api/auth', \
    description='This contains routes for core app data access. Authorization is required for each of the calls. \
    To get this authorization, please contact out I.T Team ', \
    path='/v1/')

signup = apisec.namespace('/api/auth', \
    description='This contains routes for core app data access. Authorization is required for each of the calls. \
    To get this authorization, please contact out I.T Team ', \
    path='/v1/')


full_login =  apisec.model('full_login', {
    'username': fields.String(required=True, description="username"),
    'password': fields.String(required=True, description="Users Password"),

})

signupdata = apisec.model('Signup', {
    "nom": fields.String(required=True, description="Users nom"),
    "prenom":fields.String(required=True, description="Users prenom"),
    "email":fields.String(required=True, description="Users Email"),
    "login": fields.String(required=True, description="Users login"),
    "mdp": fields.String(required=True, description="Users mdp"),
    "adresse":fields.String(required=True, description="Users adresse"),
    "trigramme":fields.String(required=True, description="Users trigramme"),
    "role":fields.Integer(required=True, description="Users role"),
    "telephone":fields.String(required=True, description="Users Tel"),
    "secteur_primaire":fields.String(required=True, description="Users  sec_pri"),
    "secteur_secondaire":fields.String(required=True, description="Users sec_sec"),
    "compte_client":fields.String(required=True, description="Users compte"),
  
})




@login.doc(
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
@login.route('/auth/login')
class Login(Resource):
    @login.expect(full_login)
    def post(self):
        app.logger.info('User login with user_name')
        req_data = request.get_json()
        username=req_data['username']
        password=req_data['password']
        if username and password:
            URL="http://195.15.228.250/manager_app/login/"
            r = requests.post(url=URL,json=req_data)
            
            if r.status_code == 200 :
                data=r.json()
                
                URL="http://195.15.218.172/edluser/Agentsec/"+str(data[0]["id"])
            
                v = requests.get(url=URL)
                
                if v.status_code == 200:
                    data[0]["client_data"]=v.json()["compte_client"]
                    return {
                            'status': 1,
                            'res': data,
                        }, 200
            else:
                return {
                        'status':0,
                        'res': 'failed',
                    }, 400
        else:
                return {
                        'status':0,
                        'res': 'no data',
                    }, 403
       
        

@signup.doc(
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
@signup.route('/auth/signup')
class Signup(Resource):
    @token_required
    @signup.expect(signupdata)
    def post(self):
        signup_data = request.get_json()
        token = request.headers['Authorization']
        if token:
            if signup_data["role"] == 1 or signup_data["role"] == 2:
                URL="http://195.15.228.250/agent_app/agent/"
                headers ={"Authorization":token}
                compte=signup_data["compte_client"]
                del signup_data["compte_client"]
                r = requests.post(url=URL,headers=headers,json=signup_data)
                
                v=r.json()
                
                v[0]['mdp']=signup_data["mdp"]
                
                URL="http://195.15.218.172/participant/Client/"+compte
                q = requests.get(url=URL)
                if q.status_code == 200:
                    v[0]['compte_client']=q.json()
                else:
                    return {
                            'status':q.status_code,
                            'res': 'No account',
                        }, 200       

                if r.status_code == 200 :
                    url1="http://195.15.218.172/synchro/util/ajouter/all"
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
                        }, 200
            else:
                URL="http://195.15.228.250/admin_app/admin/"
                headers ={"Authorization":token}
                
                role=signup_data["role"]
                del signup_data["compte_client"]
                del signup_data["role"]
                del signup_data["secteur_primaire"]
                del signup_data["secteur_secondaire"]
                del signup_data["trigramme"]
                
               
                
                r = requests.post(url=URL,headers=headers,json=signup_data)
                
                v=r.json()
                
                v[0]['mdp']=signup_data["mdp"]
                v[0]['role']=role
                

                if r.status_code == 200 :
                    url1="http://195.15.218.172/synchro/util/ajouter/done"
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
                        }, 200
        else:
                return {
                        'status':0,
                        'res': 'no data',
                    }, 401


            
