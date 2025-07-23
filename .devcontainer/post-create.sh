#!/bin/bash
# エラーが発生した時点でスクリプトを終了する設定
set -e

echo "--- Restoring .NET dependencies ---"
# backendディレクトリに移動してからdotnet restoreを実行
cd /workspaces/Noumena/workspaces/backend && dotnet restore

echo "--- Restoring Node.js dependencies ---"
# frontendディレクトリに移動してからnpm installを実行
cd /workspaces/Noumena/workspaces/frontend && npm install

echo "--- Setting up Python virtual environment and installing dependencies for AI Engine ---"
cd /workspaces/Noumena/workspaces/ai-engine
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# back to root
cd /workspaces/Noumena

echo "--- Installing global Node.js packages ---"
npm install -g @google/gemini-cli

echo "--- Installing GitHub CLI ---"
apt-get update && apt-get install -y gh

echo "--- Post-create setup complete ---"