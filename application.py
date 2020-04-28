from flask import Flask, request
from flask_restful import Resource, Api
from userDetails import adminUsersInfo, allUsersInfo, userInfo

application = app = Flask(__name__)
api = Api(app)

api.add_resource(allUsersInfo, '/userDetails')
api.add_resource(userInfo, '/userDetails/<string:name>')
api.add_resource(adminUsersInfo, '/adminDetails')


if __name__ == '__main__':
    app.run(debug=True)
