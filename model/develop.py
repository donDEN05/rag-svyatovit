from sql_generator import SQL_gen

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
t = SQL_gen()

t.connect_model()
prompt = "tables:\n" + table + "\n" +"."
print(t.generate_sql(prompt))