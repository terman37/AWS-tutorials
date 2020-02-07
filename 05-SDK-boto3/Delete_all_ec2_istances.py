import boto3

ec2 = boto3.resource('ec2')
#client = boto3.client('ec2')
# client = ec2.meta.client

# Get ids of all running or stopped instances
filters = [{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}]
running_instances = ec2.instances.filter(Filters=filters)
ids = []
for instance in running_instances:
    ids.append(instance.id)
    lastone = instance.id

if len(ids) > 0:
    # Terminate them all
    ec2.instances.filter(InstanceIds=ids).terminate()

    # Wait until last one is deleted
    ec2.Instance(lastone).wait_until_terminated()

print()
print('All instances should now be terminated')
print()
print('! -- DELETE VPC MANUALLY -- !')

# following should be working but got a dependency violation at the end when trying to delete vpc itself
# I think it can be linked with routes tables, needs to be checked when more time.
# # VPC name
# myvpc_name = 'MY_VPC'
# # Retrieve Vpc based on name tag
# filters = [{'Name': 'tag:Name', 'Values': [myvpc_name]}]
# vpcs = list(ec2.vpcs.filter(Filters=filters))
# myvpc = vpcs[0]
#
#
# # detach default dhcp_options if associated with the vpc
# dhcp_options_default = ec2.DhcpOptions('default')
# if dhcp_options_default:
#     dhcp_options_default.associate_with_vpc(VpcId=myvpc.id)
#
# # delete our security groups
# for sg in myvpc.security_groups.all():
#     if sg.group_name != 'default':
#         sg.delete()
#
# # detach and delete all gateways associated with the vpc
# for gw in myvpc.internet_gateways.all():
#     myvpc.detach_internet_gateway(InternetGatewayId=gw.id)
#     gw.delete()
#
# # delete all route table associations
# for rt in myvpc.route_tables.all():
#     for rta in rt.associations:
#         if not rta.main:
#             rta.delete()
#
# # delete subnets and network interfaces
# for subnet in myvpc.subnets.all():
#     for interface in subnet.network_interfaces.all():
#         interface.delete()
#     subnet.delete()
#
# # delete our endpoints
# for ep in client.describe_vpc_endpoints(
#         Filters=[{
#             'Name': 'vpc-id',
#             'Values': [myvpc.id]
#         }])['VpcEndpoints']:
#     client.delete_vpc_endpoints(VpcEndpointIds=[ep['VpcEndpointId']])
#
# # delete any vpc peering connections
# for vpcpeer in client.describe_vpc_peering_connections(
#         Filters=[{
#             'Name': 'requester-vpc-info.vpc-id',
#             'Values': [myvpc.id]
#         }])['VpcPeeringConnections']:
#     ec2.VpcPeeringConnection(vpcpeer['VpcPeeringConnectionId']).delete()
#
# # delete non-default network acls
# for netacl in myvpc.network_acls.all():
#     if not netacl.is_default:
#         netacl.delete()
#
# vpcid = myvpc.id
# myvpc = None
#
# # finally, delete the vpc
# client.delete_vpc(VpcId=vpcid)


