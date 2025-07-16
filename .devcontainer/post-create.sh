#!/bin/bash
# エラーが発生した時点でスクリプトを終了する設定
set -e

echo "--- Restoring .NET dependencies ---"
# backendディレクトリに移動してからdotnet restoreを実行
cd /workspace/backend && dotnet restore

echo "--- Restoring Node.js dependencies ---"
# frontendディレクトリに移動してからnpm installを実行
cd /workspace/frontend && npm install

cd ..
npm install -g @google/gemini-cli
