from flask_restx import Namespace, Resource, fields
from . import apisec

apiinfo = apisec.model('Info', {
    'name': fields.String,
    'version': fields.Integer,
    'date': fields.String,
    'author': fields.String,
    'description': fields.String
})


full_login =  apisec.model('full_login', {
    'email': fields.String(required=True, description="Email"),
    'password': fields.String(required=True, description="Users Password"),
    'login_type':fields.Boolean(required=True, description="determine_login"),

})



