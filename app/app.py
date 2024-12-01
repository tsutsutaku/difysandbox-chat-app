import requests
import streamlit as st


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
code = st.text_area(
    "コードを入力してください",
    height=200,
    value="""def main() -> dict:
    return {
        "hello": "world"
    }

print(main())""",
)

# ネットワークアクセス設定
enable_network = st.checkbox("ネットワークアクセスを許可")

# 実行ボタン
if st.button("実行"):
    with st.spinner("コードを実行中..."):
        result = run_sandbox_code(language, code, enable_network)

        # 結果の表示
        st.subheader("実行結果:")
        if "error" in result:
            st.error(f"エラーが発生しました: {result['error']}")
        else:
            # APIレスポンスの構造に合わせて修正
            if result.get("data"):
                if result["data"].get("stdout"):
                    st.code(result["data"]["stdout"])
                if result["data"].get("error"):
                    st.error(result["data"]["error"])
