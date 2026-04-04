from transformers import T5ForConditionalGeneration, T5Tokenizer

class TextTranslator():
    def __init__(self):
        self.model_name = None
        self.tokenizer = None
        self.model = None
        self.config = None

    @classmethod
    def connect_model(self, model_name='utrobinmv/t5_translate_en_ru_zh_small_1024',
                            cache_dir='model/weights',
                            device_map='auto'):
        self.model_name  = model_name

        self.tokenizer = T5Tokenizer.from_pretrained(model_name, 
                                                     cache_dir=cache_dir)
        
        self.model = T5ForConditionalGeneration.from_pretrained(model_name, 
                                                           cache_dir=cache_dir,
                                                           device_map=device_map
                                                           )
        return print('Done connect model')

    @classmethod
    def translate_text(self, input_text, max_new_tokens=None):
        input_text = 'translate to eng: ' + input_text

        inputs = self.tokenizer(input_text, 
                                return_tensors="pt").to('cuda')

        outputs = self.model.generate(**inputs, 
                                      max_new_tokens=max_new_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)