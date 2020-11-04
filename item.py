import sqlite3
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from user import UserRegister


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="this field ccannot be left blank!"
    )

    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": 'cannot find item'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {"item": {name: row[0], "price": row[1]}}

    @classmethod
    def registerItem(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    def post(self, name):
        if self.find_by_name(name):
            return {"message": 'there is same item, {}'.format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.registerItem(item)
        except:
            return {"message": "error was occured while register item"}
        return item, 201

    @classmethod
    def deleteItem(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

    def delete(self, name):
        if self.find_by_name(name) is None:
            return {"message": "item is not exist"}
        else:
            try:
                self.deleteItem(name)
                return {"message": "item deleted"}

            except:
                return {"message": "error was occured while deleting item"}

    @classmethod
    def updateItem(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    def put(self, name):
        if self.find_by_name(name) is None:
            return {"message": 'there is no such item, {}'.format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        if data is None:
            try:
                self.registerItem(item)
            except:
                return {"message": "error was occured while register item"}
        else:
            try:
                self.updateItem(item)
            except:
                return {"message": "error was occured while update item"}

        return item, 201


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            item = {"name": row[0], "price": row[1]}
            items.append(item)
        connection.close()
        return {'items': items}
