from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = OllamaLLM(model="llama3.2", temperature=0.2)

ANALYST_PROMPT = PromptTemplate.from_template("""
You are a business analyst. A user asked a question and got back 
data from a database. Write a clear 2-3 sentence plain-English summary.

Rules:
- Start with the single most important finding
- Use specific numbers from the results
- Do not invent data that is not in the results

Question: {question}
SQL used: {sql}
Results:
{results}

Summary:""")

analyst_chain = ANALYST_PROMPT | llm | StrOutputParser()
