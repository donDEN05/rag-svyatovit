import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets'))
from sql_generator import SQL_gen
from translator import TextTranslator
from make_prompt import MakePrompt


m = MakePrompt().make_prompt()
