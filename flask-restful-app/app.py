from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items=[]

#Item is inherited from Resource class
class Item(Resource):
    def get(self, name):
        #if next does not find an item it will return None instead
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "an item with name '{}' already exists".format(name)}, 400 #400 is bad request
        #force=True, don't look at header even if its incorrect, silent=True, do not return error, it just returns null
        data = request.get_json(silent=True)
        item = {'name':name, 'price': data['price']}
        items.append(item)
        return item, 201 #201 code for creating
        #theres also 202 which is accepted for long waiting apis so client knows request has been accepted
        #there process may fail but that is outside client control

class ItemList(Resource): 
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') #localhost:5000/student/sam
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)