from db_tools import Tools
import pandas as pd


class SQLMARK():
    def __init__(self):
        self.base = None
    

    @classmethod
    def sql_to_mark(self, query):
        tools = Tools()
        tools.connect()
        data_tuples = tools.execute(query)
        data = pd.DataFrame(data_tuples).fillna('NULL')
        tools.close()
        return data.to_markdown(index=False)
