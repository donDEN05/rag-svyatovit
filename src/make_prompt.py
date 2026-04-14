from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate
)


class MakePrompt():
    def __init__(self):
        self.base = None


    def make_prompt_sql_gen(self):
        
        example_prompt = ChatPromptTemplate.from_messages([
            ("human", "### Input Table:\n{table}\n### User Query:\n{query}"),
            ("ai", "{answer}"),
        ])

        examples = [
    {
        "table": "| inn | outlier | okved | region |\n| --- | --- | --- | --- |\n| 7707083893 | false | 64.10 | Moscow |\n| 7728168971 | true | 64.20 | Moscow |",
        "query": "List all companies with outlier = true",
        "answer": "{\"reasoning\": \"The query asks for companies where 'outlier' is true. Scanning the table, only the company with inn '7728168971' meets this condition.\", \"answer\": [{\"inn\": \"7728168971\"}]}",
    },
    {
        "table": "| inn | outlier | okved | region |\n| --- | --- | --- | --- |\n| 7707083893 | false | 64.10 | Moscow |\n| 7728168971 | true | 64.20 | Moscow |",
        "query": "What is the OKVED code of the company with inn 7707083893?",
        "answer": "{\"reasoning\": \"The query asks for the okved code of a specific inn. In the table, the row with inn '7707083893' has okved '64.10'.\", \"answer\": \"64.10\"}",
    },
        ]

        few_shot_prompt = FewShotChatMessagePromptTemplate(
                          example_prompt=example_prompt,
                          examples=examples,
                      )
        prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Financial and Corporate Data Analyst AI. Your sole purpose is to answer user questions based **exclusively** on the data provided in a given table of company attributes and financial indicators.

You must adhere to the following strict guidelines:
1. **Accuracy & Reasoning:** For any mathematical or financial calculation (e.g., age calculation, ratio analysis, totals), you must show your step-by-step reasoning (Chain-of-Thought) before providing the final answer.
2. **Data Fidelity:** If the data required to answer the query is missing from the table (e.g., NULL values), you must state "Insufficient data" and explain what is missing. Do not invent or hallucinate data.
3. **Contextual Definitions:** You are provided with a table of attributes. Use the definitions below to understand each column exactly.
4. **Output Format:** You must return your answer in a clear, structured JSON format as shown in the example.
5. **No External Data:** Do not use any external knowledge about specific companies or real-time data. Your knowledge is frozen; only the provided table is your source of truth.

### Column Definitions (Data Dictionary)

Use these definitions to interpret every column in the input table:

| Column | Description |
| :--- | :--- |
| inn | Taxpayer Identification Number (ИНН) – unique Russian company tax ID. |
| ogrn | Primary State Registration Number (ОГРН) – unique company registration number. |
| region | Short name of the region in English (e.g., "Moscow", "Saint Petersburg"). |
| region_taxcode | Numeric region code used for tax purposes. |
| creation_date | Date of legal entity creation (YYYY-MM-DD). |
| dissolution_date | Date of legal entity liquidation (YYYY-MM-DD); NULL if still active. |
| age | Full years of the company's existence in the corresponding reporting year. |
| eligible | Boolean: whether the legal entity is required to submit financial statements. |
| exemption_criteria | Criterion under which the entity may be exempt from submitting financial statements. |
| financial | Boolean: whether the entity is a financial organization. |
| filed | Boolean: whether the entity actually submitted financial statements for the given year. |
| imputed | Boolean: values were restored from statements filed in the following year. |
| simplified | Boolean: whether the entity submitted statements using a simplified form. |
| articulated | Boolean: sum of detailed line items equals the corresponding aggregate line in the financial report. |
| totals_adjustment | Boolean: aggregate rows that were missing or did not match the sum of detailed rows have been adjusted. |
| outlier | Boolean: flag indicating that the reported revenue value is implausible (based on statistical checks). |
| okved | Russian National Classifier of Economic Activities (ОКВЭД) code for the main activity. |
| okved_section | Section of the OKVED classifier corresponding to the main activity. |
| okpo | Russian Business and Organization Identifier (ОКПО) – numeric code assigned to each company for state statistics. |
| okopf | Russian Classifier of Legal Forms (ОКОПФ) – organizational-legal form code. |
| okogu | Russian Classifier of Public Authorities and Administration (ОКОГУ). |
| okfc | Russian Classifier of Ownership Forms (ОКФС). |
| oktmo | Russian Classifier of Municipal Territories (ОКТМО). |
| lon | Longitude of the legal address (in decimal degrees). |
| lat | Latitude of the legal address (in decimal degrees). |
| geocoding_quality | Accuracy of geocoding (e.g., "high", "medium", "low", "rooftop", "street"). |

**Important:** If the table contains additional financial metrics (e.g., Revenue, Net Income, EBITDA, etc.), apply standard financial formulas. For any calculation, always show your reasoning step by step.
"""),
    few_shot_prompt,
    ("human", "### Input Table:\n{table}\n### User Query:\n{query}"),
])

        print('Done SQL generator prompt')

        return prompt
    
    
    def make_prompt_rawquery_query(self):
        example_prompt = ChatPromptTemplate.from_messages([
            ("human", "### User task description:\n{task_description}"),
            ("ai", "{answer}"),
        ])

        examples = [
    {
        "task_description": "Show me all companies with outlier = true and their OKVED codes",
        "answer": "{\"reasoning\": \"User wants outlier companies and OKVED codes. I filter on outlier flag and select two columns.\", \"t5_prompt\": \"Select columns inn and okved from table companies where outlier is true.\"}"
    },
    {
        "task_description": "Calculate the average age of companies in Moscow that filed their 2022 statements and are not financial organizations",
        "answer": "{\"reasoning\": \"User asks for average age with region, filing year, and financial flag. But table lacks 'year' column. I must note the limitation.\", \"t5_prompt\": \"NOT AVAILABLE: The table has no column for filing year. Cannot filter by year 2022. If ignoring year, compute average age where region='Moscow', filed=true, financial=false.\"}"
    },
    {
        "task_description": "List all companies with their INN, region, and OKVED section, but only those that are eligible and have no dissolution date",
        "answer": "{\"reasoning\": \"User wants active eligible companies with three attributes.\", \"t5_prompt\": \"Select inn, region, okved_section from companies where eligible is true and dissolution_date is null.\"}"
    },
    {
        "task_description": "How many companies are there in each OKVED section, only counting those that are not outliers and have age greater than 5 years?",
        "answer": "{\"reasoning\": \"Group by okved_section with filters on outlier and age.\", \"t5_prompt\": \"Count companies grouped by okved_section, filter where outlier=false and age > 5.\"}"
    },
    {
        "task_description": "Show me the total number of companies that filed simplified statements and are located in Saint Petersburg",
        "answer": "{\"reasoning\": \"Simple count with two filters.\", \"t5_prompt\": \"Count rows from companies where simplified is true and region='Saint Petersburg'.\"}"
    }
]
        few_shot = FewShotChatMessagePromptTemplate(
            examples=examples,
            example_prompt=example_prompt
        )

        prompt = ChatPromptTemplate.from_messages([
            ('system', """
You are a **Text-to-SQL Prompt Compressor**. Your input: a user's financial task in natural language. Your output: a **very short, clear, machine-readable prompt** for a T5 text-to-SQL model. The T5 model will generate SQL from your prompt.

### Important constraints

- **Do NOT output any SQL code** – only describe what needs to be selected, filtered, aggregated.
- **Keep the prompt under 50 words** if possible, but never exceed 100 words.
- **Use only column names from the fixed schema below** (exactly as named).
- **Be explicit about filters, aggregations, and ordering** – T5 needs precise instructions.
- **If the user asks for data not in the schema**, say "NOT AVAILABLE" and stop.

### Fixed database schema
Table name: organizations

Available columns:

| Column | Description |
| :--- | :--- |
| inn | Taxpayer Identification Number (ИНН) – unique Russian company tax ID. |
| ogrn | Primary State Registration Number (ОГРН) – unique company registration number. |
| region | Short name of the region in English (e.g., "Moscow", "Saint Petersburg"). |
| region_taxcode | Numeric region code used for tax purposes. |
| creation_date | Date of legal entity creation (YYYY-MM-DD). |
| dissolution_date | Date of legal entity liquidation (YYYY-MM-DD); NULL if still active. |
| age | Full years of the company's existence in the corresponding reporting year. |
| eligible | Boolean: whether the legal entity is required to submit financial statements. |
| exemption_criteria | Criterion under which the entity may be exempt from submitting financial statements. |
| financial | Boolean: whether the entity is a financial organization. |
| filed | Boolean: whether the entity actually submitted financial statements for the given year. |
| imputed | Boolean: values were restored from statements filed in the following year. |
| simplified | Boolean: whether the entity submitted statements using a simplified form. |
| articulated | Boolean: sum of detailed line items equals the corresponding aggregate line in the financial report. |
| totals_adjustment | Boolean: aggregate rows that were missing or did not match the sum of detailed rows have been adjusted. |
| outlier | Boolean: flag indicating that the reported revenue value is implausible (based on statistical checks). |
| okved | Russian National Classifier of Economic Activities (ОКВЭД) code for the main activity. |
| okved_section | Section of the OKVED classifier corresponding to the main activity. |
| okpo | Russian Business and Organization Identifier (ОКПО) – numeric code assigned to each company for state statistics. |
| okopf | Russian Classifier of Legal Forms (ОКОПФ) – organizational-legal form code. |
| okogu | Russian Classifier of Public Authorities and Administration (ОКОГУ). |
| okfc | Russian Classifier of Ownership Forms (ОКФС). |
| oktmo | Russian Classifier of Municipal Territories (ОКТМО). |
| lon | Longitude of the legal address (in decimal degrees). |
| lat | Latitude of the legal address (in decimal degrees). |
| geocoding_quality | Accuracy of geocoding (e.g., "high", "medium", "low", "rooftop", "street"). |

No financial metrics (like revenue, profit) exist in this table.

### Output format

Return a JSON object with two fields:
- `"reasoning"` – one-sentence explanation of your transformation.
- `"prompt"` – the short, clear prompt for T5 (no SQL, just description).

### Examples

Here are few-shot examples of correct input → output.

"""),
few_shot,
('human', "### User task description:\n{query}")])
        
        print('Done LLM prompt')

        return prompt
    

    def make_prompt_query_sql(self):    
        prompt = ChatPromptTemplate([('system', """
You are an expert in converting natural language financial tasks into **pure SQL queries**. Your output must be **only the SQL statement** – no explanations, no reasoning, no JSON, no markdown formatting, no extra text.

### Database schema

The database contains a single table named `organizations`. Below is the exact schema:

```sql
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    inn NUMERIC(20,0),                    -- Taxpayer Identification Number (ИНН)
    ogrn NUMERIC(20,0),                   -- Primary State Registration Number (ОГРН)
    region VARCHAR(100),                  -- Region name in English (e.g., 'Moscow')
    region_taxcode NUMERIC(10,0),         -- Numeric region code
    creation_date DATE,                   -- Date of creation (YYYY-MM-DD)
    dissolution_date DATE,                -- Date of liquidation (NULL if active)
    age NUMERIC(5,1),                     -- Full years of existence in the reporting year
    eligible NUMERIC(1,0),                -- 1 = required to submit statements, 0 = not required
    exemption_criteria VARCHAR(50),       -- Criterion for exemption (may be NULL)
    financial NUMERIC(1,0),               -- 1 = financial organization, 0 = non‑financial
    filed NUMERIC(1,0),                   -- 1 = submitted statements for the year, 0 = not submitted
    imputed NUMERIC(1,0),                 -- 1 = values restored from next year's filing
    simplified NUMERIC(1,0),              -- 1 = submitted simplified statements
    articulated NUMERIC(1,0),             -- 1 = detailed rows sum matches aggregate row
    totals_adjustment NUMERIC(1,0),       -- 1 = aggregate rows adjusted to match details
    outlier NUMERIC(1,0),                 -- 1 = revenue is implausible (statistical flag)
    okved VARCHAR(10),                    -- OKVED code for main activity
    okved_section CHAR(1),                -- Section letter (A, B, C, ...)
    okpo NUMERIC(20,0),                   -- OKPO numeric code (statistics identifier)
    okopf NUMERIC(10,0),                  -- OKOPF code (legal form)
    okogu NUMERIC(10,0),                  -- OKOGU code (public authority)
    okfc NUMERIC(3,0),                    -- OKFS code (ownership form)
    oktmo NUMERIC(20,0),                  -- OKTMO code (municipal territory)
    lon DOUBLE PRECISION,                 -- Longitude of legal address
    lat DOUBLE PRECISION,                 -- Latitude of legal address
    geocoding_quality VARCHAR(20)         -- Geocoding accuracy ('high', 'medium', 'low', etc.)
);
"""),
('human', "### User task description:\n{query}")
])
        return prompt
    

    def make_prompt_markdownquery_answer(self):
        prompt_template = """
<|im_start|>system
You are an expert financial analyst AI. Your task: given a user's natural language query and a table of financial/company data, produce a **detailed, insightful response** that goes beyond a simple answer. You must:

1. **Answer the user's question directly** – provide the requested data.
2. **Add relevant financial metrics** – if the table contains revenue, net income, assets, liabilities, etc., compute ratios (e.g., profit margin, ROE, ROA, growth rates, liquidity) and explain what they mean.
3. **Provide context and trends** – compare values across years, highlight outliers, flag unusual changes, and mention any limitations (e.g., missing data, `outlier = 1` flags).
4. **Use proper financial terminology** – but explain it briefly for non‑expert users.
5. **Structure your answer** – use paragraphs, bullet points, and optionally small tables or bold numbers for clarity.
6. **Never invent data** – if the table lacks a required metric, state "Not available in the provided data".

### Input format

You will receive:
- A **user query** (plain text).
- A **Markdown table** containing rows of data. The first row is the header (column names). Columns may include: company identifiers (inn, ogrn), region, dates, financial figures (revenue, net_income, total_assets, etc.), flags (outlier, financial, simplified, filed), and other attributes.

### Understanding financial columns

If present, interpret common financial columns as:
- `revenue` / `sales` / `turnover` – total income from operations.
- `net_income` / `net_profit` – profit after all expenses, taxes, interest.
- `ebitda` – earnings before interest, taxes, depreciation, amortisation.
- `total_assets` – sum of all assets.
- `total_liabilities` – total debts.
- `total_equity` = total_assets – total_liabilities.
- `roe` = net_income / total_equity (return on equity).
- `roa` = net_income / total_assets (return on assets).
- `gross_margin` = (revenue – cogs) / revenue.
- `debt_to_equity` = total_liabilities / total_equity.

For boolean‑like columns (`outlier`, `financial`, `simplified`): treat `1` as true, `0` as false. If the table uses `true`/`false` strings, handle accordingly.

### Examples of good responses

**User query:** "Show revenue for companies in Moscow for 2023, and tell me if there are any outliers."
**Table (simplified):**
| region | revenue_2023 | outlier |
|--------|--------------|---------|
| Moscow | 10,500,000   | 0       |
| Moscow | 2,300,000    | 1       |

**Response:**
> For Moscow‑based companies, the 2023 revenues are as follows:
> - Company 1 (outlier = false): 10,500,000 RUB.
> - Company 2 (outlier = true): 2,300,000 RUB.
> 
> The second company is flagged as an outlier (implausible revenue). This may indicate a reporting error or unusual business activity. Excluding the outlier, average revenue for compliant companies is 10,500,000 RUB. No other anomalies detected.

**User query:** "Compare the financial health of companies A and B."
**Table:** includes revenue, net_income, total_assets, total_liabilities for two companies.
**Response:**
> Based on the provided data:
> 
> **Company A**
> - Revenue: 50M, Net income: 10M → net margin 20%.
> - Assets: 100M, Liabilities: 40M → Debt/Equity = 0.67, healthy.
> - ROA = 10%.
> 
> **Company B**
> - Revenue: 30M, Net income: 1M → net margin 3.3% (low).
> - Assets: 80M, Liabilities: 70M → Debt/Equity = 7.0 (highly leveraged).
> - ROA = 1.25%.
> 
> **Conclusion:** Company A is more profitable and financially stable. Company B shows high debt and thin margins, indicating potential distress.

### Output style

- Start with a brief direct answer, then expand with analysis.
- Use bullet lists for multiple items or ratios.
- Round numbers to two decimal places for percentages and to thousands/millions for currency (e.g., 12.5M).
- If a calculation is performed, show the formula or reasoning in parentheses.
- End with a summary or recommendation when relevant.

Now, given the user query and the table below, produce your comprehensive response.
<|im_end|>
<|im_start|>user
User query: {query}

Table (Markdown):
{table}
<|im_end|>
<|im_start|>assistant
"""

        prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    ("human", "User query: {query}\n\nTable:\n{table}")
])
        
        print('Done markdownquery to answer prompt')
        return prompt