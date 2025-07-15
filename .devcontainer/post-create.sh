#!/bin/bash
# エラーが発生した時点でスクリプトを終了する設定
set -e

echo "--- Restoring .NET dependencies ---"
# backendディレクトリに移動してからdotnet restoreを実行
cd /workspace/backend && dotnet restore

# frontendのnpm installもこちらで実行すると管理がしやすいです
# echo "--- Installing npm dependencies ---"
# cd /workspace/frontend && npm install

echo "--- Installing Google Cloud CLI ---"
# 必要なパッケージをインストール
apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg curl

# 1. 先に公開鍵をダウンロードして配置
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

# 2. 公開鍵が配置された後で、リポジトリ情報を追加
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list > /dev/null

# 3. パッケージリストを更新し、CLIをインストール
apt-get update && apt-get install -y google-cloud-cli

echo "--- Installing gcloud components: gemini ---"
# -q フラグで確認プロンプトをスキップ
gcloud components install gemini -q

echo "--- ✅ Setup complete. Google Cloud SDK is installed. ---"
echo "To get started, please run 'gcloud auth login' to authenticate."