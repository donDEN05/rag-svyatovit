import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))
from sql_generator import SQL_gen
from translator import TextTranslator
from make_prompt import MakePrompt
from sql_to_markdown import SQLMARK
from langchain_ollama.llms import OllamaLLM


class Pipeline():
    def __init__(self):
        self.translator=TextTranslator()
        self.sql_gen=SQL_gen()
        self.sql_mark=SQLMARK()
        self.make_prompt=MakePrompt()
        self.llm=OllamaLLM(model='qwen3:8b')
    
    def create_markdown(self, 
            query):
        translation = self.translator.translate_text(query)
        sql_select = self.sql_gen.generate_sql(translation)
        markdown = self.sql_mark.sql_to_mark(sql_select)

        return markdown