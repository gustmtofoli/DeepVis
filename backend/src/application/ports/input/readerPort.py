from abc import ABC, abstractmethod

class ReaderPort(ABC):

    @abstractmethod
    def read_project(self):
        pass