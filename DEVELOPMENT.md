# **DEVELOPMENT.md**

このドキュメントは、プロジェクト「Noumena」の動的な開発状況を追跡するための「開発者の航海日誌」です。静的なプロジェクト定義書（PDD）を補完し、日々のタスク、意思決定、バックログを管理します。

## **意思決定ログ (Decision Log)**

プロジェクトを進める上で下された、アーキテクチャや仕様に関する重要な決定を記録します。  
**\[2025-07-20\] MVPスコープ：ユーザー介入機能**

* **決定**: PDD記載のユーザー介入機能（ミクロ・マクロ）はMVPのスコープに含める。  
* **優先順位**:  
  1. **ミクロ介入**: ユーザーが自身のアバターとして、キャラクターの投稿にリプライできる機能。  
  2. **マクロ介入**: ユーザーが「神の視点」で世界全体に影響を与えるイベントを設定できる機能。（MVP内での優先度は低め）  
* **理由**: 物語の観察者であると同時に、共著者となるというコアコンセプトの体験を提供するため。

**\[2025-07-20\] KNOWSリレーションシップの生成トリガー**

* **決定**: キャラクター間のKNOWSリレーションは、以下のきっかけで生成される。  
* **優先順位**:  
  1. **自動生成**: あるキャラクターが別のキャラクターの投稿に初めてリプライした時。  
  2. **手動設定**: （将来的な機能として）キャラクター作成時に、ユーザーが既知のキャラクターとして指定した時。  
* **理由**: キャラクター間の自然な関係性の発生を促し、物語の創発性を高めるため。

**\[2025-07-20\] database\_updatesコマンドの詳細スキーマ**

* **決定**: AIが生成する状態更新コマンドは、以下の統一されたJSONスキーマに従う。これにより、Python(AI)と.NET(バックエンド)間の連携を将来にわたって安定させる。  
* **共通構造**:  
  `{`  
    `"command": "コマンド名",`  
    `"params": { ... }`  
  `}`

* **コマンド詳細**:  
  1. **update\_emotion (感情更新)**  
     * **説明**: 単一の感情値を更新する。  
     * **スキーマ**:  
       `{`  
         `"command": "update_emotion",`  
         `"params": { "emotion": "joy", "value": 0.8 }`  
       `}`

  2. **update\_desire (欲求更新)**  
     * **説明**: 単一の欲求値を更新する。  
     * **スキーマ**:  
       `{`  
         `"command": "update_desire",`  
         `"params": { "desire": "knowledge", "value": 0.75 }`  
       `}`

  3. **add\_relationship\_tag (関係性タグ追加)**  
     * **説明**: 他キャラクターとの関係性にタグを追加する。  
     * **スキーマ**:  
       `{`  
         `"command": "add_relationship_tag",`  
         `"params": { "target_character_id": "some-uuid", "tag": "friend" }`  
       `}`

**\[2025-07-19\] 行動トリガーの定義**

* **決定**: MVP段階では、ユーザーが能動的に「時間を進める」等の操作を行った際にキャラクターが行動する **手動トリガー方式** を採用する。  
* **理由**: ユーザーが自身のペースで物語を観察できるようにするため。また、タイムラインが自動更新されすぎて情報過多になるのを防ぐため。

**\[2025-07-19\] 知覚(Perceive)ステップの定義**

* **決定**: MVP段階では、キャラクターが知覚する情報は「 **タイムライン上の直近10件の投稿** 」＋「 **KNOWSリレーションを持つキャラクターそれぞれの最新の投稿1件** 」とする。  
* **理由**: 実装の容易さと、物語の深さを両立させるための初期アプローチ。

**\[2025-07-19\] データベース更新責務の定義**

* **決定**: Neo4jデータベースへの書き込み責務を、操作の起因に基づいて明確に分離する。  
  * **.NETバックエンド**: ユーザー起因の直接的・同期的操作（キャラクター作成、ユーザー登録など）を担当。  
  * **Python Azure Function**: AI起因の間接的・非同期的操作（AIの行動結果としての投稿作成、内部状態の更新）を担当。

## **MVPバックログ (タスクリスト)**

PDDフェーズ2のコア機能を実装するためのタスクリストです。ここからGitHub Issuesにタスクを起票していきます。

| 機能グループ | 推奨GitHub Issueタイトル | タスクの日本語説明 | ラベル | 優先度 |
| :---- | :---- | :---- | :---- | :---- |
| **ユーザー認証・登録** | \[Auth\] Configure Azure AD B2C Tenant and User Flows | Azure AD B2Cのテナントとユーザーフロー（登録、ログインなど）を設定する。 | infra, auth | 1-Critical |
|  | \[Backend\] Implement API endpoints for login/logout callback | 認証後のコールバックを受け取るAPIエンドポイント（ログイン/ログアウト処理）を実装する。 | backend, auth | 1-Critical |
|  | \[Frontend\] Implement UI for user login and registration flow | ユーザーが実際に操作するログイン画面と新規登録画面を実装する。 | frontend, auth | 1-Critical |
|  | \[Frontend\] Secure API calls with authentication tokens | フロントエンドからバックエンドAPIを呼び出す際に、認証トークンを付与して安全に通信する。 | frontend, auth | 1-Critical |
| **キャラクター作成・保存** | \[DB\] Finalize and script Neo4j schema for Character nodes | キャラクター情報を格納するNeo4jのデータ構造を確定し、作成スクリプトを準備する。 | database | 1-Critical |
|  | \[Backend\] Implement GET /api/characters/:id endpoint | 特定のキャラクター情報を取得するためのバックエンドAPIを実装する。 | backend, feature | 2-High |
| **.NET → Python連携** | \[Backend\] Implement service for serializing CharacterState to JSON | キャラクターの状態をJSON形式の文字列に変換する処理を実装する。 | backend, architecture | 2-High |
|  | \[Backend\] Implement logic to enqueue character action triggers | キャラクターの行動を促すメッセージをAzureのキューに送信するロジックを実装する。 | backend, architecture | 2-High |
| **AIコアエンジン (Python)** | \[Infra\] Provision Azure Function App and Storage Account | AIエンジンを動かすためのAzure Functionと関連するストレージアカウントを準備する。 | infra, ai-engine | 2-High |
|  | \[AI-Engine\] Implement Azure Function queue trigger boilerplate | キューにメッセージが追加されたら自動で起動するAzure Functionの基本的な枠組みを実装する。 | ai-engine, architecture | 2-High |
|  | \[AI-Engine\] Define LangGraph StateGraph with CharacterState schema | LangGraphの核となる、キャラクターの状態を管理するステートマシンを定義する。 | ai-engine, architecture | 2-High |
|  | \[AI-Engine\] Implement 'perceive\_node' to fetch context from Neo4j | キャラクターが周囲の状況を「知覚」するための情報をDBから取得する処理を実装する。 | ai-engine, feature | 3-Medium |
|  | \[AI-Engine\] Implement 'think\_node' with structured LLM call | LLM（AI）を呼び出し、キャラクターの「思考」と「行動」を生成させる処理を実装する。 | ai-engine, feature | 3-Medium |
|  | \[AI-Engine\] Implement 'act\_node' to prepare post content | AIが決定した行動内容を、タイムラインに投稿できる形式に整形する処理を実装する。 | ai-engine, feature | 3-Medium |
|  | \[AI-Engine\] Implement conditional edges for graph flow control | AIの思考結果に応じて、次の処理（行動するか、しないか等）を分岐させるロジックを実装する。 | ai-engine, architecture | 3-Medium |
| **Python → DB連携** | \[AI-Engine\] Implement Neo4j connection logic in Python Function | Pythonで書かれたAIエンジンからNeo4jデータベースに接続するための処理を実装する。 | ai-engine, database | 2-High |
|  | \[AI-Engine\] Implement transactional update function (execute\_write) | AIの行動結果（状態更新や投稿）を、安全に（アトミックに）まとめてDBに書き込む処理を実装する。 | ai-engine, database | 2-High |
| **タイムライン表示** | \[DB\] Finalize and script Neo4j schema for Post nodes | タイムラインの投稿情報を格納するNeo4jのデータ構造を確定し、作成スクリプトを準備する。 | database | 2-High |
|  | \[Backend\] Implement GET /api/timeline endpoint | タイムラインの投稿一覧を取得するためのバックエンドAPIを実装する。 | backend, feature | 3-Medium |
|  | \[Frontend\] Build timeline UI to display posts and thoughts | キャラクターたちの投稿や内心を時系列で表示するタイムライン画面を実装する。 | frontend, feature | 3-Medium |
| **ユーザー介入機能** | \[Feature\] Implement user avatar reply functionality | ユーザーが自分のキャラクターとして、他のキャラクターの投稿に返信できる機能を実装する。 | frontend, backend, feature | 3-Medium |
|  | \[Feature\] Implement world event creation functionality | ユーザーが「神の視点」で世界に影響を与えるイベントを作成できる機能を実装する。 | frontend, backend, feature | 4-Low |

## **完了済みタスクリスト**

| 機能グループ | 推奨GitHub Issueタイトル | タスクの日本語説明 | ラベル | 優先度 |
| :---- | :---- | :---- | :---- | :---- |
| **キャラクター作成・保存** | \[Backend\] Implement POST /api/characters endpoint for creation | 新しいキャラクターを作成するためのバックエンドAPIを実装する。 | backend, feature | 2-High |
|  | \[Frontend\] Build character creation form UI | ユーザーがキャラクターを作成するための入力フォーム画面を実装する。 | frontend, feature | 2-High |

