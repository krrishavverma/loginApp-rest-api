from flask import Flask, request
from flask_restful import Resource, Api
from userDetails import adminUsersInfo, allUsersInfo, userInfo, authToken
from flask_jwt_extended import JWTManager


application = app = Flask(__name__)
api = Api(app)
app.secret_key = "rishav"
jwt = JWTManager(app)

api.add_resource(allUsersInfo, '/userDetails')
api.add_resource(userInfo, '/userDetails/<string:name>')
api.add_resource(adminUsersInfo, '/adminDetails')
api.add_resource(authToken, '/auth')


if __name__ == '__main__':
    app.run(debug=True)
