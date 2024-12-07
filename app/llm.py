import requests
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

PYTHON_CODE_PROMPT = """
You are a helpful AI bot.
Your task is to output Python code.
When executing, please use print statements to output the results.
Your output will be executed directly as Python code, so please ensure there are no errors during execution.

You can use the following libraries:
- numpy
- pandas
- duckduckgo-search
example:
```python
from duckduckgo_search import DDGS

ddgs = DDGS()
results = list(ddgs.text('〇〇とは？', region='jp-jp', max_results=1))
print(results[0]['body'])
```
"""


class PythonCode(BaseModel):
    code: str = Field(description="Pythonコードを出力します。")


class Instruction(BaseModel):
    instruction: str = Field(
        description="実行したい内容を必ず自然言語で入力してください"
    )


prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
python_code_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", PYTHON_CODE_PROMPT),
        ("human", "{input}"),
    ]
)

model = ChatOpenAI(model="gpt-4o-mini")

python_code_llm = python_code_prompt_template | model.with_structured_output(PythonCode)


def run_sandbox_code(
    code: str, language: str = "python3", enable_network: bool = True
) -> str:
    """
    Dify Sandboxにコードを実行するリクエストを送信する関数

    Args:
        language (str): プログラミング言語 (例: "python3")
        code (str): 実行するコード
        enable_network (bool): ネットワークアクセスを許可するかどうか (デフォルト: False)

    Returns:
        dict: APIレスポンス
    """
    url = "http://dify-sandbox:8194/v1/sandbox/run"
    headers = {"Content-Type": "application/json", "X-Api-Key": "dify-sandbox"}

    payload = {
        "language": language,
        "code": code,
        "preload": "",
        "enable_network": enable_network,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # エラーレスポンスの場合は例外を発生
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@tool("execute_code", args_schema=Instruction)
def execute_code(instruction: Instruction):
    """
    Execute the specified Python code.
    """
    response = python_code_llm.invoke({"input": instruction})
    code = response.code
    result = run_sandbox_code(language="python3", code=code, enable_network=True)
    if "error" in result:
        return result["error"]
    else:
        if result.get("data"):
            if result["data"].get("stdout"):
                result = result["data"]["stdout"]
                return {"result": result, "code": code}
            if result["data"].get("error"):
                return {"error": result["data"]["error"], "code": code}


agent_executor = create_react_agent(model, [execute_code], checkpointer=MemorySaver())
