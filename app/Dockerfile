FROM python:3.12-slim

WORKDIR /app

# 依存関係のインストールを先に行う
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# streamlitのデフォルトポートを公開
EXPOSE 8501

# streamlitでアプリを起動
CMD ["streamlit", "run", "app.py"]
