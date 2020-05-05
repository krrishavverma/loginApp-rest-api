from flask_restful import Resource, reqparse
from flask import request
import json
from db_function import admin_users, all_users, post_db_item, patch_db_item, get_db_item, delete_db_item, auth_token_update, auth_token_delete, get_auth_token
from data_validation import user_data_validation
from flask_jwt_extended import create_access_token, jwt_required



class authToken(Resource):

    def get(self):
        token = get_auth_token()
        if token:
            return token
        return ("No token exist")

    def post(self):
        access_token = create_access_token(identity="rishav")
        auth_token_update(self, access_token)
        return {"access_token": access_token}
    

    def delete(self):
        auth_token_delete(self)


class adminUsersInfo(Resource):

    @jwt_required
    def get(self):
        admin_user = admin_users(self)
        if admin_user:
            return admin_user
        else:
            return("Not a admin user")    


class allUsersInfo(Resource):

    @jwt_required
    def get(self):
        all_user = all_users(self)
            
        if all_user:
            return all_user
        else:
            return("No user find")


class userInfo(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('password',
                        type=str,
                        required=True)
    parser.add_argument('firstname',
                        type=str,
                        required=True)
    parser.add_argument('lastname',
                        type=str,
                        required=True)
    parser.add_argument('email',
                        type=str,
                        required=True)
    parser.add_argument('gender',
                        type=str,
                        required=True)
    parser.add_argument('dateofbirth',
                        type=str,
                        required=True)
    parser.add_argument('phone',
                        type=int,
                        required=True)
    parser.add_argument('address',
                        type=str,
                        required=True)

    @jwt_required
    def get(self, name):
        user_detail = get_db_item(self, name)
        return user_detail


    def post(self, name):
        new_user = userInfo.parser.parse_args()

        new_user_detail = {
            'username': name,
            'password': new_user['password'],
            'firstname': new_user['firstname'],
            'lastname': new_user['lastname'],
            'email': new_user['email'],
            'gender': new_user['gender'],
            'dateofbirth': new_user['dateofbirth'],
            'phone': new_user['phone'],
            'address': new_user['address']
        }

        valid_info = user_data_validation(self, new_user_detail)

        if valid_info == True:
            msg = post_db_item(self, new_user_detail)
            return msg
        else:
            return valid_info, 400


    @jwt_required
    def put(self, name):
        new_user = userInfo.parser.parse_args()
        valid_info = user_data_validation(self, new_user)

        if valid_info == True:
            msg = patch_db_item(self, new_user, name)
            return msg
        else:
            return valid_info, 400


    @jwt_required
    def delete(self, name):
        msg = delete_db_item(self, name)
        if msg is None:
            return ("Caught exception : Requested resource not found while deleting data from user_details table"), 400
        else:
            return msg
            