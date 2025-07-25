#!/bin/bash
# エラーが発生した時点でスクリプトを終了する設定
set -e

# Dev Containerが提供するワークスペースのルートパスを使用
WORKSPACE_ROOT="${containerWorkspaceFolder:-/workspace}"

echo "--- Restoring .NET dependencies ---"
# backendディレクトリに移動してからdotnet restoreを実行
cd "${WORKSPACE_ROOT}/workspaces/backend" && dotnet restore

echo "--- Restoring Node.js dependencies ---"
# frontendディレクトリに移動してからnpm installを実行
cd "${WORKSPACE_ROOT}/workspaces/frontend" && npm install

echo "--- Setting up Python virtual environment and installing dependencies for AI Engine ---"
cd "${WORKSPACE_ROOT}/workspaces/ai-engine"
# 仮想環境が存在しない場合のみ作成
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
# 仮想環境内のpipを直接使用してパッケージをインストール
./.venv/bin/pip install --no-cache-dir --upgrade pip
./.venv/bin/pip install --no-cache-dir -r requirements.txt

# back to root
cd "${WORKSPACE_ROOT}"

echo "--- Installing global Node.js packages ---"
npm install -g @google/gemini-cli

echo "--- Installing GitHub CLI ---"
# apt-get updateにも-yフラグを追加し、キャッシュをクリーンアップ
apt-get update -y && apt-get install -y --no-install-recommends gh && rm -rf /var/lib/apt/lists/*

echo "--- Post-create setup complete ---"