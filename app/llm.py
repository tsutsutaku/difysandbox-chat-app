from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class PythonCode(BaseModel):
    code: str = Field(description="Pythonコードを出力します。")


SYSTEM_PROMPT = """
You are a helpful AI bot.
Your task is to output Python code.
When executing, please use print statements to output the results.
Your output will be executed directly as Python code, so please ensure there are no errors during execution.

You can use the following libraries:
- numpy
- duckduckgo-search
example:
```python
from duckduckgo_search import DDGS

ddgs = DDGS()
results = list(ddgs.text('〇〇とは？', region='jp-jp', max_results=1))
print(results[0]['body'])
```
"""


chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini")

python_code_llm = chat_template | llm.with_structured_output(PythonCode)
