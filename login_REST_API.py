from flask import Flask
from flask_restful import Api
from userDetails import adminUsersInfo, allUsersInfo, userInfo

login_api = Flask(__name__)
new_api = Api(login_api)

new_api.add_resource(allUsersInfo, '/userDetails')
new_api.add_resource(userInfo, '/userDetails/<string:name>')
new_api.add_resource(adminUsersInfo, '/adminDetails')


if __name__ == '__main__':
    login_api.run(port=5000, debug=True)