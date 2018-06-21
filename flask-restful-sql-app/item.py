import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

#Item is inherited from Resource class
class Item(Resource):
    parser = reqparse.RequestParser() #parses the request so only allowed content gets passed!
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="this field cannot be left blank"
    )
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'],item['name']))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

   

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "an item with name '{}' already exists".format(name)}, 400 #400 is bad request
        
        data = Item.parser.parse_args()
        item = {'name':name, 'price': data['price']}

        try:
            self.insert(item)
        except Exception:
            return {"message": "An error occurred inserting the item: {0}".format(Exception)}, 500 #internal server error
        
        return item, 201

    @jwt_required()
    def delete(self, name):
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()

            return {'message': 'Item deleted'}
        return {'message': "no item with name: '{}' exists in database".format(name)}, 404 
    
    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data['price']}

        if item is None: 
            try:
                self.insert(updated_item)
            except Exception:
                return {"message": "An error occurred updating the item: {0}".format(Exception)}, 500 #internal server error
        else:
            try:
                self.update(updated_item)
            except Exception:
                return {"message": "An error occurred updating the item: {0}".format(Exception)}, 500 #internal server error 
        return updated_item

class ItemList(Resource): 
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items=[]
        for row in result:
            items.append({'name':row[0], 'price': row[1]}) 

        connection.close()
        return {'items': items}