from flask_restful import Resource, reqparse
from flask import request
import json
from db_function import admin_users, all_users, post_db_item, patch_db_item, get_db_item, delete_db_item
from data_validation import user_data_validation


class adminUsersInfo(Resource):

    def get(self):
        admin_user = admin_users(self)

        if admin_user:
            return admin_user
        else:
            return("Not a admin user")
              


class allUsersInfo(Resource):

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
                        required=False)
    parser.add_argument('firstname',
                        type=str,
                        required=False)
    parser.add_argument('lastname',
                        type=str,
                        required=False)
    parser.add_argument('email',
                        type=str,
                        required=False)
    parser.add_argument('gender',
                        type=str,
                        required=False)
    parser.add_argument('dateofbirth',
                        type=str,
                        required=False)
    parser.add_argument('phone',
                        type=int,
                        required=False)
    parser.add_argument('address',
                        type=str,
                        required=False)

    def get(self, name):
        user_detail = get_db_item(self, name)
        return user_detail


    def post(self, name):
        new_user = userInfo.parser.parse_args()
        if new_user['password'] is None or new_user['firstname'] is None or new_user['lastname'] is None or new_user['email'] is None or new_user['gender'] is None or new_user['dateofbirth'] is None or new_user['phone'] is None or new_user['address'] is None:
            return {'message': 'All details are not entered'}

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

        if valid_info:
            msg = post_db_item(self, new_user_detail)
            return msg
        else:
            return {"message": "Details invalid"}


    def put(self, name):
        new_user = userInfo.parser.parse_args()
        if new_user['password'] is None or new_user['firstname'] is None or new_user['lastname'] is None or new_user['email'] is None or new_user['gender'] is None or new_user['dateofbirth'] is None or new_user['phone'] is None or new_user['address'] is None:
            return {'message': 'All details are not entered'}
        valid_info = user_data_validation(self, new_user)

        if valid_info:
            msg = patch_db_item(self, new_user, name)
            return msg
        else:
            return {"message": "Details invalid"}


    def delete(self, name):
        msg = delete_db_item(self, name)
        return msg
