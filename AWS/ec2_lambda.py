import boto3


def lambda_handler(event, context):

    init_script = ""
    ec2_client = boto3.resource('ec2')

    create_ec2 = ec2_client.create_instances(
        ImageId='ami-id',
        MaxCount=1,
        MinCount=1,
        InstanceType='c5n.4xlarge',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'kfaheem'
                    },
                    {
                        'Key': 'Project',
                        'Value': 'Capstone'
                    }
                ]
            }
        ],
        SubnetId='subnet-id',
        SecurityGroupIds=[
            'sg-1',
            'sg-2'
        ],
        IamInstanceProfile={
            'Name': 'IAM-role'
        },
        UserData=init_script
    )

    print('create_ec2 response - {}'.format(create_ec2))

    ec2_instance = create_ec2[0]
    ec2_instance.wait_until_running()
    ec2_instance.load()
