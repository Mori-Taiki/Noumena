# .devcontainer/backend.Dockerfile
# .NET 8 SDKがプリインストールされたMicrosoft提供のベースイメージを使用
FROM mcr.microsoft.com/devcontainers/dotnet:8.0

# .NET環境にPythonとNode.jsを追加インストールする
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends python3 python3-pip \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs