import requests
import streamlit as st
from llm import python_code_llm


def run_sandbox_code(language: str, code: str, enable_network: bool = False) -> dict:
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


# Streamlitアプリケーション
st.title("コード実行サンドボックス")

# 言語選択
language = st.selectbox(
    "プログラミング言語を選択",
    ["python3", "javascript", "ruby"],  # 利用可能な言語を追加
)

# コード入力エリア
input = st.text_area("実行したい内容を入力してください", height=200)

output = python_code_llm.invoke({"input": input})

# 実行ボタン
if st.button("コード生成"):
    # 生成されたコードを保存
    st.session_state.generated_code = output.code
    st.session_state.show_code = True

# 生成されたコードがある場合は常に表示
if "show_code" in st.session_state and st.session_state.show_code:
    st.subheader("生成されたコード:")
    st.code(st.session_state.generated_code)

    # 実行ボタン
    if st.button("実行する"):
        with st.spinner("コードを実行中..."):
            result = run_sandbox_code(
                language, st.session_state.generated_code, enable_network=True
            )

            # 結果の表示
            st.subheader("実行結果:")
            if "error" in result:
                st.error(f"エラーが発生しました: {result['error']}")
            else:
                if result.get("data"):
                    if result["data"].get("stdout"):
                        st.code(result["data"]["stdout"])
                    if result["data"].get("error"):
                        st.error(result["data"]["error"])
