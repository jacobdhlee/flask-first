import sqlite3
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from models.item import ItemModel


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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": 'cannot find item'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": 'there is same item, {}'.format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.registerItem()
        except:
            return {"message": "error was occured while register item"}
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            ItemModel.deleteItem()

        return {'message': 'Item deleted'}, 204

    def put(self, name):
        if ItemModel.find_by_name(name) is None:
            return {"message": 'there is no such item, {}'.format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if data is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.registerItem()

        return item.json(), 201


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
