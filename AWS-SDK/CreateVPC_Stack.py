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
