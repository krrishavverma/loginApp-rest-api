import boto3
from boto3.dynamodb.conditions import Key
import json
from dynamodb_json import json_util


dynamodb_resource = boto3.resource('dynamodb', region_name='us-west-2')

dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')


def admin_users(self):
    adminDetails = []

    try:
        response = dynamodb_client.scan(TableName='rkumar-admin-details')

        try:
            admins = response['Items']
            for admin in admins:
                admin = json_util.loads(admin)
                
                adminDetails.append(admin)
            return (adminDetails), 200
        except KeyError:
            return("No item find")
        except Exception as e:
            return e, 400
    
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        return ("Caught exception : {} while getting data from admin_details table".format(e.response.get("Error", None).get("Message", None))), 400 
    except Exception as e:
        return e


def all_users(self):
    usersDetails = []

    try:
        response = dynamodb_client.scan(TableName='rkumar-users-details')

        try:
            users = response['Items']
            for user in users:
                user = json_util.loads(user)
                
                usersDetails.append(user)
            return (usersDetails)
        except KeyError:
            return ("No item find")
        except Exception as e:
            return (e)
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        return ("Caught exception : {} while getting data from user_details table".format(e.response.get("Error", None).get("Message", None))), 400
    except Exception as e:
        return e


def post_db_item(self, data):

    try:
        name = data["username"]

        response = dynamodb_client.get_item(
        Key={
            'username': {
                'S': name,
            }
        },
        TableName='rkumar-users-details',
        )

        try:
            db_data = response['Item']
            return ("username already exist")

        except KeyError:
            new_response = dynamodb_client.get_item(
                Key={
                    'username': {
                        'S': name,
                    }
                },
                TableName='rkumar-admin-details',
                )
            
            try:
                admin_data = new_response['Item']
                return ("username already exist")
            
            except KeyError:

                table = dynamodb_resource.Table('rkumar-users-details')
                print(table)
                table.put_item(
                    Item = data
                )
                return data
        except Exception as e:
            return e
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        return ("Caught exception : {} while adding user to the user_details table".format(e.response.get("Error", None).get("Message", None))), 400
    except Exception as e:
        return e


def patch_db_item(self, data, name):

    try:

        response = dynamodb_client.get_item(
        Key={
            'username': {
                'S': name,
            }
        },
        TableName='rkumar-users-details',
        )

        try:
            db_data = response['Item']

            updated_user = {
            'username': name,
            'password': data['password'],
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'email': data['email'],
            'gender': data['gender'],
            'dateofbirth': data['dateofbirth'],
            'phone': data['phone'],
            'address': data['address']
            }

            table = dynamodb_resource.Table('rkumar-users-details')
            table.put_item(
                Item = updated_user
            )
            return updated_user

        except KeyError:
            return {"message": "username {} does not exist".format(name)}
        except Exception as e:
            return e
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        return ("Caught exception : {} while updating data to user_details table".format(e.response.get("Error", None).get("Message", None))), 400
    except Exception as e:
        return e


def get_db_item(self, name):
    try:
        response = dynamodb_client.get_item(
        Key={
            'username': {
                'S': name,
            }
        },
        TableName='rkumar-users-details',
        )

        try:
            userDeatil = response['Item']
            userDeatil = json_util.loads(userDeatil)

            return userDeatil

        except KeyError:
            return({"message": "User {} not exist".format(name)})
        except Exception as e:
            return e

    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        ("Caught exception : {} while getting data from user_details table".format(e.response.get("Error", None).get("Message", None))), 400
    
    except Exception as e:
        return e


def delete_db_item(self, name):
    try:
        table = dynamodb_resource.Table('rkumar-users-details')
        table.delete_item(
            Key = {
                'username': name
            }
        )

        return {"message": "User {} deleted".format(name)}
    except dynamodb_client.exceptions.ResourceNotFoundException as e:
        ("Caught exception : {} while deleting data from user_details table".format(e.response.get("Error", None).get("Message", None))), 400
    
    except Exception as e:
        return e, 400


def get_auth_token():
    response = dynamodb_client.scan(TableName='rkumar-auth-token')

    try:
        token_value = response['Items']
        token_value= json_util.loads(token_value)

        if (len(token_value) != 0):
            return (token_value), 200
        else:
            return False
    except KeyError:
        return("No item find")
    except Exception as e:
        return e, 400


def auth_token_update(self,token_value):
    table = dynamodb_resource.Table('rkumar-auth-token')
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'token_value': each['token_value']
                }
            )
    
    data = {"token_value": token_value}  
    table = dynamodb_resource.Table('rkumar-auth-token')
    table.put_item(
            Item = data
        )


def auth_token_delete(self):
    table = dynamodb_resource.Table('rkumar-auth-token')
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'token_value': each['token_value']
                }
            )
