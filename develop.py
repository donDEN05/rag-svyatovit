import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets'))
from src.translator import TextTranslator

s = TextTranslator()
print(s.translate_text('выбери лучшую цену по инн учитывая регион инн'))