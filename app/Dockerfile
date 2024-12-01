FROM python:3.12-slim

WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY app.py .

# streamlitのデフォルトポートを公開
EXPOSE 8501

# streamlitでアプリを起動
CMD ["streamlit", "run", "app.py"]
