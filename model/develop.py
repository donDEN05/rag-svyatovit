import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasets'))


from sql_to_markdown import SQLMARK

s = SQLMARK()
s.sql_to_mark('select * from organizations;')