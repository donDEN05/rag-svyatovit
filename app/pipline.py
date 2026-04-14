import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from sql_generator import SQL_gen
from translator import TextTranslator
from make_prompt import MakePrompt
from sql_to_markdown import SQLMARK
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
import json


class Pipeline():
    def __init__(self):
        self.translator=TextTranslator()
        self.sql_gen = SQL_gen()
        self.sql_mark = SQLMARK()
        self.make_prompt = MakePrompt()
        self.llm = OllamaLLM(model='qwen3:8b',
                           temperature=0,
                           top_p=0.95
                           )
        self.query = None
    

    def _query_markdown(self, 
            query):
        prompt_sql = self.make_prompt.make_prompt_query_sql()
        chain_sql = prompt_sql | self.llm | StrOutputParser()
        llm_output = chain_sql.invoke({'query': query})
        print(llm_output)
        if 'NOT AVAILABLE' in llm_output:
            print('Поменяйте запрос')
            return 'NOT AVAILABLE: can not extrack table '
        markdown = self.sql_mark.sql_to_mark(llm_output)

        return markdown


    def _rawquery_query(self, query):
        translated_query = self.translator.translate_text_to_eng(query)
        self.query = translated_query
        prompt_llm = self.make_prompt.make_prompt_rawquery_query()
        chain_llm = prompt_llm | self.llm | StrOutputParser()
        llm_output = chain_llm.invoke({'query': translated_query})
        llm_output = json.loads(llm_output)
        llm_output_parsed = llm_output.get("prompt")
        
        return llm_output_parsed
    

    def _markdownquery_answer(self, markdown):
        prompt = self.make_prompt.make_prompt_markdownquery_answer()

        chain = prompt | self.llm | StrOutputParser()
        answer = chain.invoke({'query': self.query, 'table': markdown})

        return answer
    

    def run(self, input):
        query = self._rawquery_query(input)
        markdown = self._query_markdown(query)
        answer = self._markdownquery_answer(markdown)

        return answer