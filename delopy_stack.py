import boto3


def cloudformation_client():
    cloudformation = boto3.client('cloudformation')
    return cloudformation


def create_cfn_stack():
    cfn_template_url = 'https://rkumarec2instance.s3.amazonaws.com/user_details_db.yaml'
    cloudformation_client().update_stack(
        StackName = 'rkumar-login-app',
        TemplateURL = cfn_template_url
    ) 


if __name__ == '__main__':
    create_cfn_stack()
