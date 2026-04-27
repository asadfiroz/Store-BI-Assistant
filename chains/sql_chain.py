from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = OllamaLLM(model="llama3.2", temperature=0)

SQL_PROMPT = PromptTemplate.from_template("""
You are an expert MySQL analyst. Using ONLY the schema below, write a 
single valid MySQL query that answers the user's question.

Rules:
- Return ONLY the raw SQL query
- No explanation, no markdown, no backticks
- Use proper MySQL syntax
- Every column reference MUST use the alias of the table it belongs to
- Never reference an alias that was not defined in the FROM or JOIN clause
- Only use aliases that are explicitly defined in your query
- Limit to 100 rows unless asking for totals or counts

Schema:
{schema}

Examples of correct queries:

Example 1 - revenue by category:
SELECT p.category, SUM(oi.unit_price * oi.quantity) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC

Example 2 - count by region:
SELECT c.region, COUNT(c.customer_id) AS customer_count
FROM customers c
GROUP BY c.region
ORDER BY customer_count DESC

Example 3 - order status count:
SELECT o.status, COUNT(o.order_id) AS total_orders
FROM orders o
GROUP BY o.status

Question: {question}

SQL Query:""")

sql_chain = SQL_PROMPT | llm | StrOutputParser()
