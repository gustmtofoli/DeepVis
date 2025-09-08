from abc import ABC, abstractmethod

class ParserPort(ABC):
    @abstractmethod
    def parse_ast(self, code):
        pass