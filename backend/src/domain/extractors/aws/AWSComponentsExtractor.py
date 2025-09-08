import json

class AWSComponentsExtractor:

    def extract_aws_nodes(self, ast, graph=None, parent=None, secret_name=None, global_ast=None, programming_language=None, is_first_node=False):
        if not programming_language:
            raise Exception("Programming language not found")
        
        ast_config = {
            "JavaScript": {
                'node_type': 'type',
                'search_node_type': 'NewExpression'
            },
            "Python": {
                'node_type': '_type',
                'search_node_type': 'Call'
            },
            "Java": {
                'node_type': 'type',
                'search_node_type': 'Custom'
            }
        }

        aws_sdk_v3_config = {
            "JavaScript": {
                'SecretsManager': ["GetSecretValueCommand"],
                'SQS': ["SendMessageCommand"],
                'DynamoDB': ["PutCommand", "ScanCommand"],
                'SES': ['SendEmailCommand'],
                'SNS': ['PublishCommand'],
                'S3': ['GetObjectCommand'],
                'SSM': ['GetParameterCommand']
            },
            "Python": {
                'SQS': ["sqs"],
                'DynamoDB': ["dynamodb"]
            },
            "Java": {
                'SecretsManager': ['AWSSecretsManager'],
                'SQS': ['SQSConnection'],
                'SES': ['AmazonSimpleEmailService'],
                'SNS': ['AmazonSNSClient'],
                'S3': ['S3Client']
            }
        }

        components = {}
        
        if isinstance(ast, dict):
            # print(">>> ast_config[programming_language]['node_type']: ", ast_config[programming_language]['node_type'])
            for service_name, service_commands in aws_sdk_v3_config[programming_language].items():
                for command in service_commands:
                    parent = self.__extract_aws_component(
                        ast=ast,
                        node_type=ast.get(ast_config[programming_language]['node_type'], ""), 
                        node_id=service_name, 
                        search_node_type=ast_config[programming_language]['search_node_type'], 
                        search_command_name=command
                    )

                    if parent:
                        components[command] = parent

            for _, value in ast.items():
                if isinstance(value, (dict, list)):
                    components.update(self.extract_aws_nodes(value, graph, parent, secret_name, global_ast=global_ast, programming_language=programming_language))

        elif isinstance(ast, list):
            for item in ast:
                components.update(self.extract_aws_nodes(item, graph, parent, secret_name, global_ast=global_ast, programming_language=programming_language))

        return components

    def __extract_aws_component(self, ast, node_type, node_id, search_node_type, search_command_name):
        try:
            ast_search = json.dumps(ast)
        except:
            ast_search = str(ast)

        if node_type == search_node_type and search_command_name in ast_search:
            return node_id