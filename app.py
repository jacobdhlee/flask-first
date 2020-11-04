from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "abcdefghijklmnop"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/signup')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
