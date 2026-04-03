import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets'))
from db_tools import Tools


t = Tools()
t.connect()
t.close()