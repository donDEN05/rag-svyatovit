import psycopg2


class Tools():
    def __init__(self):
        self.conn = None
        self.cursor = None


    def connect(self, host='localhost', port=5432, dbname='svyatovit', user='donden', password='3535'):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        return print('Done connect')


    def create(self, template_path='datasets/create_db.sql'):
        self.cursor = self.conn.cursor()

        with open(template_path, encoding='utf-8') as f:
            sql = f.read()
            self.cursor.execute(sql)
        
        self.conn.commit()

        return print('Done create')
    

    def fill(self, csv_path='datasets/data_to_fill.csv', table_name='organizations'):
        with open(csv_path, encoding='utf-8') as f:
            self.cursor.copy_from(f, table_name, sep=',', null='')
        
        return print('Done fill')
    

    def close(self):
        self.conn.close()
        self.cursor.close()

        return print('Closed')


t = Tools()
t.connect()
t.close()
