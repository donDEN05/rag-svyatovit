from db_tools import Tools
import pandas as pd


class SQLMARK():
    def __init__(self):
        self.base = None


    def sql_to_mark(self, query):
        tools = Tools()
        tools.connect()
        data_tuples = tools.execute(query)
        columns = tools.column_names()
        data = pd.DataFrame(data_tuples, columns=columns).fillna('NULL')

        tools.close()
        print('Markdown Done')
        return data.to_markdown(index=False)
