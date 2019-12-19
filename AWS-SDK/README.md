# AWS SDK - Python

### Credentials

Get keys from Vocareum account (Account Details):

<img src="credentials_vocareum.png" alt="credentials_vocareum" style="zoom:50%;" />

if not existing create and edit `c:/users/<user>/.aws/credentials`

​	copy/paste from Vocareum

```te
[default]
aws_access_key_id=<key>
aws_secret_access_key=<key>
#aws_session_token=<key>
```

if not existing create and edit `c:/users/<user>/.aws/config`

```
[default]
region = us-east-1
```

### Install AWS packages

- Install [Toolkit](https://aws.amazon.com/fr/pycharm/) for PyCharm (allows easier credentials management from PyCharm)

  <img src="aws_toolkit.png" alt="aws_toolkit" style="zoom:50%;" />

- Install needed packages

```bash
pip install awscli
pip install boto3
```

### Python script (VPC)

Create VPC - IGW - 2 subnets (private/public)

<img src="example_vpc.png" alt="example_vpc" style="zoom:50%;" />

```python
import boto3

# Std configuration 1 vpc with subnet 1 private and subnet 2 public
# ------------------------------------------
cIDR_VPC = '192.168.0.0/16'
cIDR_Sub1 = '192.168.10.0/24'
cIDR_Sub2 = '192.168.20.0/24'
# ------------------------------------------

ec2 = boto3.resource('ec2')

# create VPC
vpc = ec2.create_vpc(CidrBlock=cIDR_VPC)
vpc.wait_until_available()
vpc.create_tags(Tags=[{"Key": "Name", "Value": "MY_VPC"}])

# create an internet gateway and attach it to VPC
IGW = ec2.create_internet_gateway()
IGW.create_tags(Tags=[{"Key": "Name", "Value": "MY_IGW"}])
vpc.attach_internet_gateway(InternetGatewayId=IGW.id)

# create subnet1 (private)
subnet1 = ec2.create_subnet(CidrBlock=cIDR_Sub1, VpcId=vpc.id)
subnet1.create_tags(Tags=[{"Key": "Name", "Value": "SubNet1_Private"}])

# create subnet2 (public)
subnet2 = ec2.create_subnet(CidrBlock=cIDR_Sub2, VpcId=vpc.id)
subnet2.create_tags(Tags=[{"Key": "Name", "Value": "SubNet2_Public"}])

# Find main route table
main_route_table = []
for route_table in vpc.route_tables.all():
    for association in route_table.associations:
        if association.main:
            main_route_table.append(route_table)
RT_main = main_route_table[0]
RT_main.create_tags(Tags=[{"Key": "Name", "Value": "Route_Private"}])

# create a route table 
RT_public = vpc.create_route_table()
RT_public.create_tags(Tags=[{"Key": "Name", "Value": "Route_Public"}])

# Add a public route to route table
# Default route table created for VPC is private
route = RT_public.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=IGW.id)

# Associate RT_public with subnet 2 to make it public
RT_public.associate_with_subnet(SubnetId=subnet2.id)

# Associate RT_main with subnet 1 (not necessary as RT_main is default RT)
RT_main.associate_with_subnet(SubnetId=subnet1.id)
```

### Python script (VPC with Cloudformation Stack)

Same but with Cloudformation stack

```python
import boto3

def main(stackname, template):
    cf = boto3.client('cloudformation')
    with open(template, 'r') as file:
        template_body = file.read()

    # valid = cf.validate_template(TemplateBody=template_body)
    cf.create_stack(StackName=stackname,
                    TemplateBody=template_body,
                    ResourceTypes=[
                        'AWS::*',
                    ])

if __name__ == "__main__":
    stack_name = "MY"
    template_file = "VPC_Stack.yaml"
    main(stack_name, template_file)
```

using Yaml template:

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: >-
  Network Template: Create VPC, 1 public / 1 private subnet

# This template creates:
#   VPC
#   Internet Gateway
#   Public Subnet
#    - Public Route Table
#   Private Subnet

######################
# Resources section
######################

Resources:

  ## VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      EnableDnsSupport: true
      EnableDnsHostnames: true
      CidrBlock: 192.168.0.0/16
      Tags:
        - Key: 'Name'
          Value: !Sub '${AWS::StackName}-VPC'
      
  ## Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: 'Name'
          Value: !Sub '${AWS::StackName}-IGW'

  VPCGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway
  
  ## Public Route Table
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: 'Name'
          Value: !Sub '${AWS::StackName}-RT-Public'
  
  PublicRoute:
    Type: AWS::EC2::Route
    DependsOn: VPCGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway
      
  ## Public Subnet
  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 192.168.20.0/24
      Tags:
        - Key: 'Name'
          Value: !Sub '${AWS::StackName}-Public-Sub'
  
  PublicSubnetRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet
      RouteTableId: !Ref PublicRouteTable
        
  ## Private Route Table
  PrivateRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: 'Name'
          Value: !Sub '${AWS::StackName}-RT-Private'
      
  ## Private Subnet
  PrivateSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 192.168.10.0/24
      Tags:
        - Key: 'Name'
          Value: !Sub '${AWS::StackName}-Private-Sub'
  
  PrivateSubnetRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnet
      RouteTableId: !Ref PrivateRouteTable
  
######################
# Outputs section
######################

Outputs:
  
  VPC:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub '${AWS::StackName}-VPCID'
  
  PublicSubnet:
    Description: Public Subnet
    Value: !Ref PublicSubnet
    Export:
      Name: !Sub '${AWS::StackName}-PublicSubnet'
      
  PrivateSubnet:
    Description: Private Subnet
    Value: !Ref PrivateSubnet
    Export:
      Name: !Sub '${AWS::StackName}-PrivateSubnet'

```



### Python script (EC2 instance)

Create an EC2 instance (t2.micro running linux) in Public Subnet created previously using security group defined to allow SSH.

```python
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
    ImageId='ami-00068cd7555f543d5',
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
 
```

