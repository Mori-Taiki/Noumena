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
# rootユーザーのためsudoは不要
apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg curl

echo 'deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main' > /etc/apt/sources.list.d/google-cloud-sdk.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

apt-get update && apt-get install -y google-cloud-cli

echo "--- Installing gcloud components: gemini ---"
gcloud components install gemini -q

echo "--- Setup complete. Google Cloud SDK is installed. ---"
echo "Please run 'gcloud auth application-default login' to authenticate."