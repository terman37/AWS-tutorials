# AWS SDK

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

### install AWS packages

```bash
pip install awscli
pip install boto3
```

### Python script (VPC related)

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

