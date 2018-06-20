from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
#production api this needs to be secure and secret for JWT
app.secret_key='sam'
api = Api(app)

jwt=JWT(app, authenticate, identity) #/auth

api.add_resource(Item, '/item/<string:name>') #localhost:5000/student/sam
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

#only run this if you run this file not when it is imported which is very important
if __name__ == '__main__':
    app.run(port=5000, debug=True)