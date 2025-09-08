from src.domain.parsers.parserPort import ParserPort
import ast
import json

class PythonParser(ParserPort):
    def __ast_to_dict(self, node):
    # Se o nó for uma instância de ast.AST, transformamos ele em um dicionário
        if isinstance(node, ast.AST):
            # Criamos um dicionário com o nome da classe do nó e seus campos
            result = {
                "_type": type(node).__name__,
            }
            for field in ast.iter_fields(node):
                name, value = field
                # Se o campo for um nó AST, chamamos a função recursivamente
                if isinstance(value, ast.AST):
                    result[name] = self.__ast_to_dict(value)
                # Se o campo for uma lista de nós AST, aplicamos a função a cada item da lista
                elif isinstance(value, list):
                    result[name] = [self.__ast_to_dict(item) if isinstance(item, ast.AST) else item for item in value]
                else:
                    result[name] = value
            return result
        # Se não for um nó AST, retornamos o valor diretamente
        return node

    def parse_ast(self, code):
        # Converter o código da função em uma árvore de sintaxe abstrata (AST)
        parsed_ast = ast.parse(code)

        ast_dict = self.__ast_to_dict(parsed_ast)

        return ast_dict, parsed_ast
