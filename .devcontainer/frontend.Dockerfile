# .devcontainer/frontend.Dockerfile
# Node.jsとTypeScriptがプリインストールされたMicrosoft提供のベースイメージを使用
FROM mcr.microsoft.com/devcontainers/typescript-node:18

# ワーキングディレクトリを設定
WORKDIR /workspace/workspaces/frontend

# 依存関係ファイルをコピー
COPY workspaces/frontend/package.json workspaces/frontend/package-lock.json* ./

# 依存関係をインストール
RUN npm install

# アプリケーションのソースコードをコピー
COPY workspaces/frontend/ ./

# 開発サーバーのデフォルトポートを公開
EXPOSE 3000