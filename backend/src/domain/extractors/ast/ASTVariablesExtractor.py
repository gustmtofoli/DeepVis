import ast as AST
import re
import json

class ASTVariablesExtractor(AST.NodeVisitor):
    def __init__(self):
        self.variables = {}

    def visit_Assign(self, node):
        # Tenta extrair o valor da variável
        value = self.get_value(node.value)
        for target in node.targets:
            if isinstance(target, AST.Name):  # Garante que seja uma variável
                self.variables[target.id] = value
        self.generic_visit(node)  # Continua percorrendo a árvore
    
    def visit_AnnAssign(self, node):
        # Trata atribuições com anotações de tipo (ex: x: int = 10)
        if isinstance(node.target, AST.Name):
            value = self.get_value(node.value) if node.value else None
            self.variables[node.target.id] = value
        self.generic_visit(node)
    
    def get_value(self, node):
        """Extrai o valor literal se possível."""
        if isinstance(node, AST.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, AST.Num):  # Python < 3.8 (compatibilidade)
            return node.n
        elif isinstance(node, AST.Str):
            return node.s
        elif isinstance(node, AST.List):
            return [self.get_value(e) for e in node.elts]
        elif isinstance(node, AST.Tuple):
            return tuple(self.get_value(e) for e in node.elts)
        elif isinstance(node, AST.Dict):
            # Retorna uma string representando o dicionário para evitar o erro
            return {self.get_value(k): self.get_value(v) for k, v in zip(node.keys, node.values)}
        elif isinstance(node, AST.Name):  # Se for outra variável
            return f"Reference to {node.id}"
        elif isinstance(node, AST.BinOp):  # Expressões como "a + b"
            return "Expression"
        return "Unknown"

    
    def extract_variables(self, ast, ast_object, programming_language):
        # variables = {}
        if programming_language == "JavaScript":
            if isinstance(ast, dict):
            
                if ast.get("type") == "VariableDeclaration":
                    for declarator in ast.get("declarations", []):
                        var_name = declarator.get("id", {}).get("name")
                        var_value = None
                        
                        if "init" in declarator and declarator["init"]:
                            init_node = declarator["init"]
                            if init_node["type"] == "Literal":
                                var_value = init_node.get("value")
                            elif init_node["type"] == "Identifier":
                                var_value = f"Reference to {init_node.get('name')}"
                            else:
                                var_value = "Complex Expression"
                            
                        if var_name:
                            self.variables[var_name] = var_value

                for _, value in ast.items():
                    if isinstance(value, (dict, list)):
                        self.variables.update(self.extract_variables(value, ast_object, programming_language))
            

            elif isinstance(ast, list):
                for item in ast:
                    self.variables.update(self.extract_variables(item, ast_object, programming_language))
        
        elif programming_language == "Python":
                self.visit(ast_object)
        elif programming_language == "Java":
            # variables = {}
            # print(ast)
            body = ast['body']
            for item in body:
                if 'customTree' in item:
                    for i in range(len(item['customTree'])):
                        customTreeArg = item['customTree'][i]
                        customTreeArg = customTreeArg.__dict__ if customTreeArg else None
                        
                        if customTreeArg:
                            customTreePackage = customTreeArg.get('package', [])
                            customTreeImports = customTreeArg.get('imports', [])
                            customTreeTypes = customTreeArg.get('types', [])


                            for customTreeType in customTreeTypes:
                                customTreeTypeDict = customTreeType.__dict__
                                
                                for bodyItem in customTreeTypeDict.get('body', []):
                                    for bodyItemBody in bodyItem.__dict__.get('body', []):
                                        for declarator in bodyItemBody.__dict__.get('declarators', []):
                                            # print(declarator.__dict__.get('name', ""))
                                            # print(declarator.__dict__.get('initializer', []).__dict__.get('value', ""))
                                            name = declarator.__dict__.get('name', "")
                                            initializer = declarator.__dict__.get('initializer', [])
                                            value = initializer.__dict__.get('value', "") if initializer else None
                                            
                                            if name and value and value != "null":
                                                self.variables[name] = value

                            # print(customTreeTypes)


        return self.variables