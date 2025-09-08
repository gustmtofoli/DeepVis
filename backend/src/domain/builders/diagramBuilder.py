from diagrams import Cluster, Diagram, Edge
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS, Eventbridge
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import SecretsManager
from diagrams.aws.compute import Lambda, EC2, ElasticBeanstalk
from diagrams.aws.mobile import APIGateway
from diagrams.aws.management import SystemsManagerParameterStore
from diagrams.generic.compute import Rack
from diagrams.onprem.compute import Server
from diagrams.custom import Custom
from diagrams.aws.engagement import SES
from diagrams.aws.integration import SNS
import json


class DiagramBuilder:

    def generate_architecture_diagram(self, component_name):
        with open('graph_data.json', 'r') as graph_data:
            graph_adj_list = json.load(graph_data)

        component_infos = {}
        nodes = graph_adj_list.get('nodes')
        for node in nodes:
            if node.get('id') == component_name:
                component_infos = node
                break
        
        title = ""
        direction = "LR"

        graph_attr = {
            "bgcolor": "#18171d"
            # "pad": "0.5",  # Ajusta o padding para melhor visualização
        }

        node_attr = {
            "fontcolor": "white"  # Define a cor da label como branca
        }

        with Diagram(title, show=False, direction=direction, filename=f"../frontend/{component_name}", graph_attr=graph_attr, node_attr=node_attr, outformat="png"):
            edge = Edge(minlen="4")
            
            if component_infos.get('type') == "AWS Lambda Function":
                start = Lambda(component_name)
            else:
                start = Server(component_name, style="filled", fillcolor="orange")
            
            diagram = start

            for successor in component_infos.get('successors').split(", "):
                diagram >> edge >> self.__get_component(successor)
            
            for predecessor in component_infos.get('predecessors').split(', '):
                component = self.__get_component(predecessor)
                if component:
                    component >> edge >> diagram


    def __get_component(self, component_name):
        component_name_compare = component_name.replace('[', '')    

        if component_name_compare:
            if component_name_compare.startswith("SSM"):
                component = SystemsManagerParameterStore(component_name)
            elif component_name_compare.startswith("SQS"):
                component = SQS(component_name)
            elif component_name_compare.startswith("SecretsManager"):
                component = SecretsManager(component_name)   
            elif component_name_compare.startswith("S3"):
                component = S3(component_name)
            elif component_name_compare.startswith("DynamoDB"):
                component = Dynamodb(component_name)
            elif component_name_compare.startswith("SES"):
                component = SES(component_name)
            elif component_name_compare.startswith("SNS"):
                component = SNS(component_name)
            else:
                component = Rack(component_name, fillcolor="lightblue")

            return component
