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

        return print('Done connect model')
    

    def generate_sql(self,
                     input_text,
                     max_new_tokens=512,
                    
                     ):
        
        inputs = self.tokenizer(input_text, 
                                padding=True, 
                                truncation=True, 
                                return_tensors="pt").to('cuda')
        
        outputs = self.model.generate(**inputs, 
                                      max_new_tokens=max_new_tokens,
                                      )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        