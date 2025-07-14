# .devcontainer/frontend.Dockerfile
# [cite_start]Node.jsとTypeScriptがプリインストールされたMicrosoft提供のベースイメージを使用 [cite: 89]
FROM mcr.microsoft.com/devcontainers/typescript-node:18

# 必要に応じて、ここに追加のツールをインストールするコマンドを記述できます
# (例: RUN apt-get update && apt-get install -y <ツール名>)