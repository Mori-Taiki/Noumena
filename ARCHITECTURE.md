# アーキテクチャ概要

このドキュメントは、Noumenaプロジェクトのアーキテクチャ、特にサービス間のネットワークトラフィックの流れに焦点を当てて概説します。

## ポートとデータの流れ

以下の図は、ユーザーのブラウザ、フロントエンド、バックエンド、およびデータベース間の全体的なデータの流れを示しています。

```mermaid
graph TD
    subgraph あなたのPC (ホストマシン)
        A[ブラウザ]
    end

    subgraph VS Code Dev Container (Docker環境)
        subgraph frontendコンテナ
            D[Next.js (3000番ポート)]
        end
        subgraph backendコンテナ
            E[.NET (5001番ポート)]
        end
        subgraph databaseコンテナ
            F[Neo4j (7687番, 7474番ポート)]
        end
    end

    A -- "http://localhost:3000" --> D
    A -- "http://localhost:5001/api/..." --> E
    A -- "http://localhost:7474 (Neo4jブラウザ)" --> F
    D -- "APIリクエスト" --> E
    E -- "DBクエリ" --> F

```

### 詳細なフロー

---

#### 1. フロントエンドへのアクセス

あなたがブラウザでWebアプリケーションを表示する際のデータの流れです。

1.  **ブラウザ**: `http://localhost:3000` にアクセスします。
2.  **VS Code**: `.devcontainer/devcontainer.json` の `forwardPorts` 設定に基づき、PCの`3000`番ポートへのアクセスをDocker環境に転送します。
3.  **Docker Compose**: `docker-compose.yml` の `frontend` サービスの `ports: - "3000:3000"` 設定により、転送されたアクセスを `frontend` コンテナ内の`3000`番ポートに繋ぎます。
4.  **Next.js**: `frontend` コンテナ内で待機しているNext.jsの開発サーバーがリクエストを受け取り、Webページのデータをブラウザに返します。

---

#### 2. フロントエンドからバックエンドへのAPIリクエスト

WebアプリケーションがバックエンドのAPI（例: `/api/health`）を呼び出す際のデータの流れです。

1.  **ブラウザ (JavaScript)**: フロントエンドのコードが `.env` ファイルの `NEXT_PUBLIC_BACKEND_API_URL` に基づき、`http://localhost:5001/api/health` のようなURLにAPIリクエストを送信します。
2.  **VS Code**: PCの`5001`番ポートへのアクセスをDocker環境に転送します。
3.  **Docker Compose**: `docker-compose.yml` の `backend` サービスの `ports: - "5001:5001"` 設定により、アクセスを `backend` コンテナ内の`5001`番ポートに繋ぎます。
4.  **.NET**: `backend` コンテナ内で待機している.NETアプリケーションがリクエストを受け取り、`{ "status": "Ok" }` のようなJSONデータを返します。

---

#### 3. バックエンドからデータベースへの接続

バックエンドがデータベース（Neo4j）からデータを読み書きする際のデータの流れです。**このフローはDockerネットワーク内部で完結します。**

1.  **.NET**: `backend` コンテナ内のアプリケーションが、`.env` ファイルの `NEO4J_URI` （例: `bolt://database:7687`）に基づき、データベースへの接続を試みます。
2.  **Dockerネットワーク**: `docker-compose.yml` で定義された `noumena_net` という内部ネットワークが、`database` というサービス名からIPアドレスを解決し、`database` コンテナにリクエストを転送します。
3.  **Neo4j**: `database` コンテナ内の`7687`番ポートで待機しているNeo4jが接続を受け付け、クエリを実行して結果を `backend` コンテナに返します。

このフローでは、ホストマシンからのポートフォワーディングは使用されません。コンテナ同士がサービス名で直接通信しているのがポイントです。
