-- Таблица организаций для RAG-агента по финансовым отчётностям
CREATE TABLE IF NOT EXISTS organizations (
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
);

-- Комментарии к таблице и столбцам
COMMENT ON TABLE organizations IS 'Справочник организаций для финансового RAG-агента (данные по юридическим лицам)';
COMMENT ON COLUMN organizations.inn IS 'ИНН (идентификационный номер налогоплательщика)';
COMMENT ON COLUMN organizations.ogrn IS 'ОГРН (основной государственный регистрационный номер)';
COMMENT ON COLUMN organizations.region IS 'Сокращённое название региона на английском языке';
COMMENT ON COLUMN organizations.region_taxcode IS 'Код региона';
COMMENT ON COLUMN organizations.creation_date IS 'Дата создания юридического лица';
COMMENT ON COLUMN organizations.dissolution_date IS 'Дата ликвидации юридического лица';
COMMENT ON COLUMN organizations.age IS 'Число полных лет компании в соответствующем году';
COMMENT ON COLUMN organizations.eligible IS 'Должно ли юридическое лицо сдавать бухгалтерскую отчетность (0/1)';
COMMENT ON COLUMN organizations.exemption_criteria IS 'Критерий, согласно которому юридическое лицо может не сдавать бухгалтерскую отчетность (none, state, initiated, religious, financial)';
COMMENT ON COLUMN organizations.financial IS 'Является ли юридическое лицо финансовой организацией (0/1)';
COMMENT ON COLUMN organizations.filed IS 'Сдало ли юридическое лицо бухгалтерскую отчетность в соответствующем году (0/1)';
COMMENT ON COLUMN organizations.imputed IS 'Значения восстановлены по отчетности, поданной в следующем году (0/1)';
COMMENT ON COLUMN organizations.simplified IS 'Сдача отчетности по упрощенной форме (0/1)';
COMMENT ON COLUMN organizations.articulated IS 'Сумма значений по детализированным строкам финансовой отчетности равна значению в соответствующей суммирующей строке (0/1)';
COMMENT ON COLUMN organizations.totals_adjustment IS 'Значения суммирующих строк, которые отсутствовали или не совпадали с суммами строк, которые они обобщали, были скорректированы (0/1)';
COMMENT ON COLUMN organizations.outlier IS 'Отметка о неправдоподобности значения выручки в опубликованной отчетности (0/1)';
COMMENT ON COLUMN organizations.okved IS 'ОКВЭД по основному виду деятельности';
COMMENT ON COLUMN organizations.okved_section IS 'Раздел ОКВЭД по основному виду деятельности (буква)';
COMMENT ON COLUMN organizations.okpo IS 'ОКПО (Общероссийский классификатор предприятий и организаций)';
COMMENT ON COLUMN organizations.okopf IS 'ОКОПФ (Общероссийский классификатор организационно-правовых форм)';
COMMENT ON COLUMN organizations.okogu IS 'ОКОГУ (Общероссийский классификатор органов государственной власти и управления)';
COMMENT ON COLUMN organizations.okfc IS 'ОКФС (Общероссийский классификатор форм собственности)';
COMMENT ON COLUMN organizations.oktmo IS 'ОКТМО (Общероссийский классификатор территорий муниципальных образований)';
COMMENT ON COLUMN organizations.lon IS 'Долгота юридического адреса (WGS84)';
COMMENT ON COLUMN organizations.lat IS 'Широта юридического адреса (WGS84)';
COMMENT ON COLUMN organizations.geocoding_quality IS 'Точность геокодирования (house — точный адрес, street — уровень улицы, city — уровень города)';