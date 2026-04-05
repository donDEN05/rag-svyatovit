from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate
)


class MakePrompt():
    def __init__(self):
        self.base = None


    def make_prompt_calculations(self):
        
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

        return prompt