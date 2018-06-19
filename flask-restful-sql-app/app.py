from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
#production api this needs to be secure and secret for JWT
app.secret_key='sam'
api = Api(app)

jwt=JWT(app, authenticate, identity) #/auth

items=[]

#Item is inherited from Resource class
class Item(Resource):
    parser = reqparse.RequestParser() #parses the request so only allowed content gets passed!
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="this field cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        #if next does not find an item it will return None instead
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "an item with name '{}' already exists".format(name)}, 400 #400 is bad request
        
        data = Item.parser.parse_args()
        
        item = {'name':name, 'price': data['price']}
        items.append(item)
        return item, 201 #201 code for creating
        #theres also 202 which is accepted for long waiting apis so client knows request has been accepted
        #there process may fail but that is outside client control

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        #method to update item price or name etc
        #this method checks if there is already an existing item there
        #if not add this item if there is then just update its content

        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name']==name, items), None)
        if item is None: 
            item={'name': name, 'price': data['price']}
            items.append(item)
        else: 
            #python dictionaries come with update function
            item.update(data)
        return item

class ItemList(Resource): 
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') #localhost:5000/student/sam
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)