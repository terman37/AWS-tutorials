import boto3

stack_name = "MY"

cf = boto3.client('cloudformation')

cf.delete_stack(StackName=stack_name)
