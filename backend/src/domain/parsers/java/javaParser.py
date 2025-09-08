from src.domain.parsers.parserPort import ParserPort
import javalang
import json

class JavaParser(ParserPort):

    def parse_ast(self, code_list):
        """Extrai a AST completa de um projeto Java e retorna como um JSON estruturado."""
        # java_files = glob.glob(os.path.join(project_path, '**', '*.java'), recursive=True)

        ast_structure = {"type": "Program", "body": []}

        # for java_file in java_files:
            # print(f"📂 Processando: {java_file}")
        
        count = -1
        for java_file in code_list:
            count += 1
            ast = self.extract_ast_from_java_file(java_file)
            if ast:
                ast_structure["body"].append({
                    "type": "Custom",
                    "customTree": self.node_to_dict(ast)
                })
                
                # ["type"] = "NewExpression"
                # ast_structure["callee"] = self.node_to_dict(ast)
            else:
                print(f"⚠️ Erro ao gerar a AST para {java_file}")

        # print(ast_structure)
        return dict(ast_structure), None

    def extract_ast_from_java_file(self, java_file):
        try:
            tree = javalang.parse.parse(java_file)
            return tree, None
        except Exception as e:
            print(f"Error: {e}")
        return None

    def node_to_dict(self, node):
        """Converte um nó AST do Javalang para um dicionário."""
        if isinstance(node, javalang.tree.Node):
            return {
                "type": node.__class__.__name__,
                "children": {key: self.node_to_dict(value) for key, value in node.__dict__.items() if value}
            }
        elif isinstance(node, list):
            return [self.node_to_dict(item) for item in node]
        elif isinstance(node, set):
            return list(node)
        else:
            return node
    