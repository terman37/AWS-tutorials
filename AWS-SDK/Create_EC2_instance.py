import boto3

ec2 = boto3.resource('ec2')

# Config
# **********************************************************************************
# machine name
myinstancename = 'NAT'

# AMI to use (select one)
# myami = 'ami-00068cd7555f543d5'  # Amazon Linux Ami
# myami ='ami-04b9e92b5572fa0d1' # Ubuntu 18.04 Ami
myami = 'ami-00a9d4a05375b2763' # NAT instance

# Subnet (select one) # public / private
flag_subnet = 'public'

# VPC name
myvpc_name = 'MY_VPC'

# **********************************************************************************
# Retrieve Vpc based on name tag
filters = [{'Name': 'tag:Name', 'Values': [myvpc_name]}]
vpcs = list(ec2.vpcs.filter(Filters=filters))
myvpc = vpcs[0]

# Choose subnet
if flag_subnet == 'public':
    mysubnet = 'SubNet2_Public'
else:
    mysubnet = 'SubNet1_Private'

# Retrieve Subnet based on name tag
filters = [{'Name': 'tag:Name', 'Values': [mysubnet]}]
subs = list(myvpc.subnets.filter(Filters=filters))
mysub = subs[0]

# SG with different name for each machine
mysgname = 'SG-' + myinstancename

# Create a security group and allow SSH inbound rule through the VPC
sg = ec2.create_security_group(GroupName=mysgname, Description='SG for instance:' + myinstancename, VpcId=myvpc.id)
sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
sg.create_tags(Tags=[{"Key": "Name", "Value": "SG-" + myinstancename}])

if mysubnet == 'SubNet2_Public':
    flag_publicIP = True
else:
    flag_publicIP = False

#  Create an EC2 instance
t2micro = ec2.create_instances(
    ImageId=myami,
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    KeyName='AWS-training-keypair',
    NetworkInterfaces=[{
        'DeviceIndex': 0,
        'SubnetId': mysub.id,
        'Groups': [sg.id],
        'AssociatePublicIpAddress': flag_publicIP
    }]
)

# Returns a list, my instance is the first and only one
myinstance = t2micro[0]
myinstance.create_tags(Tags=[{"Key": "Name", "Value": myinstancename}])

# Wait until instance is running before displaying OK
myinstance.wait_until_running()

print()
print('New EC2 instanced named {}, in {} successfully created and running'.format(myinstancename, mysubnet))
print('PrivateIP: {} - PublicIP: {}'.format(myinstance.private_ip_address, myinstance.public_ip_address))

# # Elastic IP Allocation (if needed)
#
# client = boto3.client('ec2')
# eip = client.allocate_address(Domain='vpc')
#
# # Wait until instance is running
# myinstance.wait_until_running()
#
# # Associate Elastic IP to created instance
# client.associate_address(InstanceId=myinstance.id, AllocationId=eip["AllocationId"])
