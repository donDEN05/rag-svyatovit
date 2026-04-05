from transformers import T5Tokenizer, T5ForConditionalGeneration


class SQL_gen():
    def __init__(self):
        self.model_name = None
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small', 
                                                     cache_dir='model/weights')
        self.model = None
        self.config = None


    def connect_model(self,
                      model_name='cssupport/t5-small-awesome-text-to-sql',
                      cache_dir='model/weights',
                      device_map='auto'):
        
        self.model_name = model_name
        
        self.model = T5ForConditionalGeneration.from_pretrained(model_name,
                      cache_dir=cache_dir,
                      device_map=device_map)

        return print('Done connect sql model')
    

    def generate_sql(self,
                     input_text,
                     max_new_tokens=None,
                     ):
        self.connect_model()
        
        table = """CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    inn NUMERIC(20,0),                    
    ogrn NUMERIC(20,0),                
    region VARCHAR(100),
    region_taxcode NUMERIC(10,0),          
    creation_date DATE,
    dissolution_date DATE,
    age NUMERIC(5,1),                     
    eligible NUMERIC(1,0),              
    exemption_criteria VARCHAR(50),
    financial NUMERIC(1,0),
    filed NUMERIC(1,0),
    imputed NUMERIC(1,0),
    simplified NUMERIC(1,0),
    articulated NUMERIC(1,0),
    totals_adjustment NUMERIC(1,0),
    outlier NUMERIC(1,0),
    okved VARCHAR(10),
    okved_section CHAR(1),
    okpo NUMERIC(20,0),                   
    okopf NUMERIC(10,0),                   
    okogu NUMERIC(10,0),                  
    okfc NUMERIC(3,0),                    
    oktmo NUMERIC(20,0),                
    lon DOUBLE PRECISION,
    lat DOUBLE PRECISION,
    geocoding_quality VARCHAR(20)
);"""
        prompt = "tables:\n" + table + "\n" + input_text
        
        inputs = self.tokenizer(prompt, 
                                padding=True, 
                                truncation=True, 
                                return_tensors="pt").to('cuda')
        
        outputs = self.model.generate(**inputs, 
                                      max_new_tokens=max_new_tokens,
                                      )
        
        print('Sql generated')
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        