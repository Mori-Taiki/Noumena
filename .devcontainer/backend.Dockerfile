# .devcontainer/backend.Dockerfile
# [cite_start].NET 8 SDKがプリインストールされたMicrosoft提供のベースイメージを使用 [cite: 89]
FROM mcr.microsoft.com/devcontainers/dotnet:8.0

# [cite_start].NET環境にPythonとpipを追加インストールする [cite: 89]
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends python3 python3-pip