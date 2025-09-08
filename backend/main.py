from src.domain.adapters.input.readerAdapter import ReaderAdapter
from src.domain.extractors.ast.ASTVariablesExtractor import ASTVariablesExtractor
from src.domain.extractors.aws.AWSComponentsExtractor import AWSComponentsExtractor
from src.domain.extractors.projecttype.ProjectTypeExtractor import ProjectTypeExtractor
# from src.domain.parsers.js.javascriptParser import JavascriptParser
from src.domain.parsers.parser import Parser
from src.domain.adapters.output.graphOutputAdapter import GraphOutputAdapter
import json
import networkx as nx
import os
import sys
from collections import defaultdict
from fastapi import FastAPI, Response, status
from src.domain.builders.diagramBuilder import DiagramBuilder
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiagramBody(BaseModel):
    nodeId: str

@app.post("/diagram")
def read_root(data: DiagramBody, response: Response):
    if not data:
        raise Exception("Bad Request")
    
    node_id = data.nodeId
    if not node_id:
        raise Exception('Bad Request')
    
    DiagramBuilder().generate_architecture_diagram(node_id)

    response.status_code = status.HTTP_200_OK

    return {
        'status': 201,
        'message': 'success'
    }


try:
    MODE = sys.argv[1]
    DIR = sys.argv[2]
except:
    raise Exception("Argument not valid")

def default_to_dict(d):
    if isinstance(d, defaultdict):
        return {k: default_to_dict(v) for k, v in d.items()}
    return d



if __name__ == "__main__":
    read_adapter = ReaderAdapter()
    # ast_variable_extractor = ASTVariablesExtractor()
    aws_components_extractor = AWSComponentsExtractor()
    project_type_extractor = ProjectTypeExtractor()
    parser = Parser()
    visualize_graph_adapter = GraphOutputAdapter()

    graph = nx.DiGraph()

    dir_list = []
    if MODE == 'individual':
        dir_list.append(DIR)
    elif MODE == 'group':
        subdirectories = [d for d in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, d))]
        dir_list = [ f'{DIR}{subdir}' if DIR.endswith('/') else f'{DIR}/{subdir}' for subdir in subdirectories ]
        # print(dir_list)
    else:
        raise Exception("Invalid mode. These are the allowed modes: individual, group")
    
    for directory in dir_list:
        PROJECT_CODE_DIR_SPLIT = directory.split("/")
        PROJECT_NAME = PROJECT_CODE_DIR_SPLIT[len(PROJECT_CODE_DIR_SPLIT)-1]

        project_type, project_language = project_type_extractor.get_project_type(directory)
        print('\n>>> project: ', project_type, project_language)

        code, code_list = read_adapter.read_project(directory)

        if code:
            ast, ast_object = parser.parse(
                programming_language=project_language, 
                code=code,
                code_list=code_list
            )

            ast_file = open("output/ast.txt", 'w')
            # print('>>>> ', type(ast))
            
            try:
                ast_file.write(json.dumps(ast))
            except:
                ast_file.write(str(ast))

            if ast:
                aws_components = aws_components_extractor.extract_aws_nodes(ast=ast, global_ast=ast, programming_language=project_language, is_first_node=True)
                variables = ASTVariablesExtractor().extract_variables(ast=ast, ast_object=ast_object, programming_language=project_language)

                # filter variables
                variable_keys = {
                    "SecretsManager": {
                        "variableNameKeys": ["secret"] 
                    },
                    "SQS": {
                        "variableNameKeys": ["queue"]
                    },
                    "DynamoDB": {
                        "variableNameKeys": ["table"]
                    },
                    "SES": {
                        "variableNameKeys": ["email"] 
                    },
                    "SNS": {
                        "variableNameKeys": ["topic"] 
                    },
                    "S3": {
                        "variableNameKeys": ["bucket"] 
                    },
                    "SSM": {
                        "variableNameKeys": ["parameter"] 
                    }
                }

                key_variations = {}
                for component in set(aws_components.values()):
                    key_variations[component] = []
                    for key in variable_keys[component]['variableNameKeys']:
                        key_variations[component].append(key)
                        key_variations[component].append(key.capitalize())
                        key_variations[component].append(key.upper())
                
                variables = { k: v for k, v in variables.items() if v not in ["Complex Expression"] }

                # Build adj_list (graph input)
                adj_list = {}
                for component in set(aws_components.values()):
                    label = f'[{component}]'
                    adj_list[component] = []
                    for variable_name, variable_value in variables.items():
                        for key_variation in key_variations[component]:
                            if key_variation in variable_name:
                                label += f' {variable_value}'
                                adj_list[component].append(label)
                
                # Build graph
                graph.add_node(PROJECT_NAME, label=PROJECT_NAME, type=project_type, language=project_language)
                for component, component_names in adj_list.items():
                    if component_names:
                        for component_name in component_names:
                            graph.add_node(component_name, label=component_name, type=f'AWS {component}')
                            graph.add_edge(PROJECT_NAME, component_name)
                    else:
                        graph.add_node(component, label=component, type=f'AWS {component}')
                        graph.add_edge(PROJECT_NAME, component)

            # print('>>> is strongly connected: ', nx.is_strongly_connected(graph))
            # print('>>> components strongly connected: ', list(nx.strongly_connected_components(graph)))
            # print('>>> is weakly connected: ', nx.is_weakly_connected(graph))
            # print('>>> components weakly connected: ', list(nx.weakly_connected_components(graph)))
            try:
                cycle = nx.find_cycle(graph, orientation="original")
            except:
                cycle = []
            # print('>>> has cycle: ',  cycle)
            degree_counts = {'degree': {}, 'in_degree': {}, 'out_degree': {}}
            for node in graph.nodes():
                degree_counts['degree'].update({node: graph.in_degree(node) + graph.out_degree(node)})
                degree_counts['in_degree'].update({node: graph.in_degree(node)})
                degree_counts['out_degree'].update({node: graph.out_degree(node)})


            # degree_counts = {node: graph.in_degree(node) + graph.out_degree(node) for node in graph.nodes()}
            max_degree = max(degree_counts['degree'].values())
            nodes_bigger_degree = [node for node, degree in degree_counts['degree'].items() if degree == max_degree]
            # print('>>> degree: ', nodes_bigger_degree)

            max_in_degree = max(degree_counts['in_degree'].values())
            nodes_bigger_in_degree = [node for node, degree in degree_counts['in_degree'].items() if degree == max_in_degree]
            # print('>>> in_degree_all: ', degree_counts['in_degree'])
            # print('>>> in_degree: ', nodes_bigger_in_degree)

            max_out_degree = max(degree_counts['out_degree'].values())
            nodes_bigger_out_degree = [node for node, degree in degree_counts['out_degree'].items() if degree == max_out_degree]
            # print('>>> out_degree: ', nodes_bigger_out_degree)

            group_attributes = ["type", "language"]
            grouped_nodes = defaultdict(list)
            for attribute in group_attributes:
                if not grouped_nodes.get(attribute):
                    grouped_nodes[attribute] = defaultdict(list)
                for node, data in graph.nodes(data=True):
                    if attribute in data:
                        # if data[attribute] in grouped_nodes[attribute]:
                        if 'components' in grouped_nodes[attribute][data[attribute]]:
                            grouped_nodes[attribute][data[attribute]]['components'].append(node)
                            grouped_nodes[attribute][data[attribute]]['count'] += 1
                        else:
                            grouped_nodes[attribute][data[attribute]] = {}
                            grouped_nodes[attribute][data[attribute]]['components'] = []
                            grouped_nodes[attribute][data[attribute]]['count'] = 1
            # print('>>> grouped_nodes: ', grouped_nodes)

            


            disconnected_components = list(nx.weakly_connected_components(graph))
            # print('>>> disconnected_components: ', disconnected_components)
            graph_properties_data = {
                'cycle': 'No cycles' if not cycle else ', '.join(cycle),
                'has_disconnected_components': json.dumps([list(s) for s in disconnected_components]) if len(disconnected_components) > 0 else 'No',
                'nodes_bigger_degree': ', '.join(nodes_bigger_degree),
                'nodes_bigger_in_degree': ', '.join(nodes_bigger_in_degree),
                'nodes_bigger_out_degree': ', '.join(nodes_bigger_out_degree),
                'total_number_of_nodes': len(graph.nodes),
                'grouped_nodes': json.dumps(default_to_dict(grouped_nodes))
            }

            with open('graph_properties_data.json', 'w') as graph_properties_file:
                json.dump(graph_properties_data, graph_properties_file)

            visualize_graph_adapter.generate_json(graph)
            print("AST visualizada em 'output/aws_ast_graph.html'")
