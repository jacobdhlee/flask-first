import sqlite3
from flask_restful import Resource, Api, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="this field ccannot be left blank!")
    parser.add_argument('password', type=str, required=True,
                        help="this field ccannot be left blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

        userExist = UserModel.find_by_username(data['username'])

        if userExist is not None:
            return {"message": "Username exist"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        qury = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(qury, (data['username'], data['password']))

        connection.commit()
        connection.close()
        return {'message': 'user is created'}, 201
