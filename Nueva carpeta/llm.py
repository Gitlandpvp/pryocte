import os
import openai
import json

openai.api_key = os.getenv('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')

class LLM():
    def __init__(self):
        pass
    
    def process_functions(self, text):
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                    {"role": "system", "content": "Eres un asistente que ayuda a las personas con discapacidades especiales"},
                    {"role": "user", "content": text},
            ], functions=[
                {
                    "name": "open_runachay",
                    "description": "Abrir el explorador Chrome en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio al cual se desea ir"
                            }
                        }
                    }
                },
            ],
            function_call="None",
        )
        
        message = response["choices"][0]["message"]
        
        if message.get("function_call"):
            function_name = message["function_call"]["name"] #Que funcion?
            args = message.to_dict()['function_call']['arguments'] #Con que datos?
            print("Funcion a llamar: " + function_name)
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message
    
    def process_response(self, text, message, function_name, function_response):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "Eres un asistente malhablado"},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return response["choices"][0]["message"]["content"]