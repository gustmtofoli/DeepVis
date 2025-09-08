from src.application.ports.input.readerPort import ReaderPort
import os

class ReaderAdapter(ReaderPort):
    def __is_code_file(self, file):
        extensions = ['.js', '.py', '.java']
        for extension in extensions:
            if file.endswith(extension):
                return True
        return False

    def read_project(self, directory):
        """Lê todo o código da Lambda a partir de múltiplos arquivos .js no diretório especificado."""
        code = ""
        code_list = []
        
        # Caminha por todos os arquivos do diretório e seus subdiretórios
        for root, dirs, files in os.walk(directory):
            for file in files:
                if self.__is_code_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            file_content = f.read()
                            code += file_content + "\n"  # Adiciona o conteúdo do arquivo
                            code_list.append(file_content)
                    except Exception as e:
                        print(f"Erro ao ler o arquivo {file_path}: {e}")
        
        if not code:
            print("Erro: Nenhum arquivo [.js, .py, .java] encontrado no diretório.")
            return None
        
        return code, code_list