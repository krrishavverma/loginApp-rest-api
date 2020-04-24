import boto3
from boto3.dynamodb.conditions import Key
import json
from dynamodb_json import json_util


dynamodb_resource = boto3.resource('dynamodb')

dynamodb_client = boto3.client('dynamodb')


def admin_users(self):
    adminDetails = []
    response = dynamodb_client.scan(TableName='rkumar-admin-details')

    try:
        admins = response['Items']
        for admin in admins:
            admin = json_util.loads(admin)
            
            adminDetails.append(admin)
        return (adminDetails)
    except KeyError:
        print("No item find")
    except Exception as e:
        print(e)


def all_users(self):
    usersDetails = []
    response = dynamodb_client.scan(TableName='rkumar-users-details')

    try:
        users = response['Items']
        for user in users:
            user = json_util.loads(user)
            
            usersDetails.append(user)
        return (usersDetails)
    except KeyError:
        print("No item find")
    except Exception as e:
        print(e)


def post_db_item(self, data):
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
            table.put_item(
                Item = data
            )
            return data
    except Exception as e:
        return e


def patch_db_item(self, data, name):

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
        # db_data = json_util.loads(db_data)

        # if data['password'] is None and data['firstname'] is None and data['lastname'] is None and data['email'] is None and data['gender'] is None and data['dateofbirth'] is None and data['phone'] is None and data['address'] is None:
        #     return {'message': 'No details are entered'}
        
        # if data['password'] is None:
        #     password = db_data['password']
        #     data['password'] = password
        
        # if data['firstname'] is None:
        #     firstname = db_data['firstname']
        #     data['firstname'] = firstname
        
        # if data['lastname'] is None:
        #     lastname = db_data['lastname']
        #     data['lastname'] = lastname
        
        # if data['email'] is None:
        #     email = db_data['email']
        #     data['email'] = email
        
        # if data['gender'] is None:
        #     gender = db_data['gender']
        #     data['gender'] = gender
        
        # if data['dateofbirth'] is None:
        #     dateofbirth = db_data['dateofbirth']
        #     data['dateofbirth'] = dateofbirth
        
        # if data['phone'] is None:
        #     phone = db_data['phone']
        #     data['phone'] = phone
        
        # if data['address'] is None:
        #     address = db_data['address']
        #     data['address'] = address

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


def get_db_item(self, name):
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


def delete_db_item(self, name):
    table = dynamodb_resource.Table('rkumar-users-details')
    table.delete_item(
        Key = {
            'username': name
        }
    )

    return {"message": "User {} deleted".format(name)}
