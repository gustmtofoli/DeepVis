from src.domain.extractors.projecttype.ProgrammingLanguageExtractor import ProgrammingLanguageDetector
import os

class ProjectTypeExtractor:
    def __init__(self):
        self.__programming_language_detector = ProgrammingLanguageDetector()
    
    def get_project_type(self, project_directory):
        project_type_indicators = {
            "JavaScript": {
                "express": {

                },
                "aws_lambda_function": {
                    "file_indicator": ["index.js"],
                    "expression_indicator": ["exports.handler"]
                }
            },
            "Python": {
                "flask": {

                },
                "fastAPI": {

                },
                "Django": {

                },
                "aws_lambda_function": {
                    "file_indicator": ["lambda_function.py"],
                    "expression_indicator": ["lambda_handler"]
                }
            },
            "Java": {
                
            }
        }

        project_language = self.__programming_language_detector.detect_language(project_directory)

        project_type_label = "Generic project type"
        
        for root, _, files in os.walk(project_directory):
            for file in files:
                for project_type in project_type_indicators[project_language].keys():
                    if file in project_type_indicators[project_language][project_type].get("file_indicator", []):
                        try:
                            with open(f"{project_directory}/{file}", "r", encoding="utf-8") as f:
                                print(project_type)
                                for expression in project_type_indicators[project_language][project_type].get("expression_indicator", []):
                                    if expression in f.read():
                                        project_type_label = "AWS Lambda Function"
                        except:
                            pass

        return project_type_label, project_language