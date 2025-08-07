from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from extensions import bcrypt, auth, jwt
from schema import schema
from dotenv import load_dotenv
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, jwt_required)
import os
from models import User, session

load_dotenv() #loads environment vairbale from .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret')
app.config['JWT_SECRET_KEY'] = os.getenv('jwtsecret')

bcrypt.init_app(app)
auth.init_app(app)
jwt.init_app(app)

@app.route('/')
def index():
    return "Graphql running..."

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=False,
        
    )
)
