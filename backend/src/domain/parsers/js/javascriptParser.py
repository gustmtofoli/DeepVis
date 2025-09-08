from src.domain.parsers.parserPort import ParserPort
import json
import subprocess

class JavascriptParser(ParserPort):
    def parse_ast(self, js_code):
        """Executa Esprima para gerar a AST do código JavaScript."""
        if not js_code.strip():
            print("Erro: Código JavaScript está vazio!")
            return None

        try:
            # Usa JSON.stringify para evitar erros de escape no código
            node_command = f'''
                const esprima = require("esprima");
                const code = {json.dumps(js_code)};
                console.log(JSON.stringify(esprima.parseScript(code, {{ range: true }})));
            '''

            # Executa o Node.js via subprocess
            result = subprocess.run(
                ['node', '-e', node_command],
                capture_output=True,
                text=True
            )

            # Verifica erro na execução do subprocess
            if result.returncode != 0:
                print(f"Erro ao executar Node.js: {result.stderr}")
                return None

            return json.loads(result.stdout), None

        except Exception as e:
            print(f"Erro ao gerar AST: {e}")
            return None