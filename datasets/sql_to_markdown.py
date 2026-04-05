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
        columns = [
            'id',
            'inn',                    
            'ogrn',                
            'region',
            'region_taxcode',          
            'creation_date',
            'dissolution_date',
            'age',                     
            'eligible',              
            'exemption_criteria',
            'financial',
            'filed',
            'imputed',
            'simplified',
            'articulated',
            'totals_adjustment',
            'outlier',
            'okved',
            'okved_section',
            'okpo',                   
            'okopf',                   
            'okogu',                  
            'okfc',                    
            'oktmo',                
            'lon',
            'lat',
            'geocoding_quality'
        ]
        data = pd.DataFrame(data_tuples, columns=columns).fillna('NULL')

        tools.close()
        return data.to_markdown(index=False)
