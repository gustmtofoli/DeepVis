import os

class ProgrammingLanguageDetector:
    def detect_language(self, directory):
        extensions = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".cs": "C#",
            ".go": "Go",
            ".rb": "Ruby",
            ".php": "PHP"
        }

        file_counts = {lang: 0 for lang in extensions.values()}

        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in extensions:
                    file_counts[extensions[ext]] += 1

        primary_language = max(file_counts, key=file_counts.get) if any(file_counts.values()) else "Desconhecida"
        return primary_language