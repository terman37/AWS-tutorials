import boto3

ec2 = boto3.resource('ec2')

myvpc_name = 'MY_VPC'
mysubnet = 'SubNet2_Public'

# Retrieve Vpc based on name tag
filters = [{'Name': 'tag:Name', 'Values': [myvpc_name]}]
vpcs = list(ec2.vpcs.filter(Filters=filters))
myvpc = vpcs[0]

# Retrieve Subnet based on name tag
filters = [{'Name': 'tag:Name', 'Values': [mysubnet]}]
subs = list(myvpc.subnets.filter(Filters=filters))
mysub = subs[0]

# Create a security group and allow SSH inbound rule through the VPC
sg = ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=myvpc.id)
sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
sg.create_tags(Tags=[{"Key": "Name", "Value": "MY_SG_for_SSH"}])

#  Create a linux instance in the subnet
t2micro = mysub.create_instances(
    # Amazon Linux Ami
    # ImageId='ami-00068cd7555f543d5',
    # Ubuntu 18.04 Ami
    ImageId='ami-04b9e92b5572fa0d1',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    KeyName='AWS-training-keypair',
    SecurityGroupIds=[sg.id]
)
# Returns a list, my instance is the first and only one
myinstance = t2micro[0]
myinstance.create_tags(Tags=[{"Key": "Name", "Value": "MY_EC2_for_SSH"}])

# Allocate Elastic IP
client = boto3.client('ec2')
eip = client.allocate_address(Domain='vpc')

# Wait until instance is running
myinstance.wait_until_running()

# Associate Elastic IP to created instance
client.associate_address(InstanceId=myinstance.id, AllocationId=eip["AllocationId"])
