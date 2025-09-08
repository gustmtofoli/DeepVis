from src.domain.parsers.js.javascriptParser import JavascriptParser
from src.domain.parsers.python.pythonParser import PythonParser
from src.domain.parsers.java.javaParser import JavaParser

class Parser:
    def parse(self, programming_language, code, code_list):
        ast = None
        
        if programming_language == "JavaScript":
            ast = JavascriptParser().parse_ast(code)
        elif programming_language == "Python":
            ast = PythonParser().parse_ast(code)
        elif programming_language == "Java":
            ast = JavaParser().parse_ast(code_list)
        
        return ast