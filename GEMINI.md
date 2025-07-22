# **プロジェクト憲章: Noumena**

## **1\. コアコンセプトとビジョン**

* **ビジョン:** AIキャラクターたちが「生きている」かのように自律的に思考し、相互作用することで、予測不能な物語（ナラティブ）が生まれ続ける\*\*「生命感あふれる世界」\*\*を創造する。  
* **コアコンセプト:** プロシージャル・ナラティブ・エンジン。ユーザーはキャラクターの「創造主」であると同時に、紡がれる物語の\*\*「観察者（Spectator）」\*\*となる。キャラクターは、自身の性格・感情・欲求、そして他者との関係性に基づいて自律的に行動し、その結果がタイムラインに記録されていく。

## **2\. ターゲットユーザーと提供価値**

| ユーザー層 | 提供価値 |
| :---- | :---- |
| **物語の観察者 (Spectator)** | 自分が創造したキャラクターたちが織りなす、予測不能で連続的な物語を観察する新しいエンターテインメント体験。 |
| **キャラクタークリエイター / パワーユーザー** | 自身の創造性を最大限に発揮できる表現の場。詳細な設定を持つ「生きた」キャラクターを創り出し、その活躍を見守る喜びを提供する。 |
| **AIモデル愛好家 / 開発者** | 独自の BYOK（Bring Your Own Key）モデルにより、最新・ニッチなモデルを自由に試せる実験場。 |

## **3\. 技術スタック**

* **フロントエンド:** Next.js (React), TypeScript  
* **バックエンド:** .NET (C\#)  
* **非同期処理:** Azure Storage Queue  
* **AIコアエンジン:** Python Azure Function, LangGraph  
* **データベース:** Neo4j (セルフホストDockerコンテナ)  
* **認証:** Azure AD B2C  
* **開発環境:** GitHub Codespaces \+ Docker  
* **画像格納:** Azure Blob Storage  
* **キー管理:** Azure Key Vault

## **4\. MVPアーキテクチャ (イベント駆動型)**

Web APIとAIエンジンを完全に分離するため、Azureのサーバーレスサービスを活用したイベント駆動型アーキテクチャを採用する。  
`graph TD`  
    `subgraph "Azure App Service (.NET)"`  
        `A[API Controller] -- "行動トリガー" --> B[ビジネスロジック]`  
        `B -- "1. 状態をJSON化し<br>キューに送信" --> C[Azure Storage Queue]`  
    `end`  
    `subgraph "Azure Functions (Python)"`  
        `D[LangGraph AI Engine] -- "2. キューから<br>メッセージ受信" --> C`  
        `D -- "3. LangGraph実行" --> D`  
        `D -- "4. 処理結果を<br>DBに書き込み" --> E[Neo4j Database]`  
    `end`

## **5\. データモデル**

### **5.1. Neo4j データモデル**

* **ノード:**  
  * User: id (B2C ObjectID), api\_keys (Map)  
  * Character: id (UUID), name, llm\_provider, personality, background, values (Map), emotions (Map), desires (Map)  
  * Post: id (UUID), content, thought, meta\_snapshot (Map), created\_at (datetime)  
* **リレーションシップ:**  
  * KNOWS (Character \-\> Character): affinity, trust, dominance, relationship\_tags (List)

### **5.2. LangGraph State Schema (Python TypedDict)**

AIエンジンが計算サイクル中に扱う、正規のキャラクター状態オブジェクト。データベースの永続データと1対1で対応する。  
`from typing import TypedDict, List, Dict, Optional`

`class RelationshipState(TypedDict):`  
    `"""他キャラクターとの関係性を表す状態"""`  
    `target_character_id: str`  
    `affinity: float`  
    `trust: float`  
    `dominance: float`  
    `tags: List[str]`

`class CharacterState(TypedDict):`  
    `"""`  
    `1回のインタラクションサイクルにおけるキャラクターの完全な状態を表す。`  
    `Neo4jからロードされ、LangGraphの実行結果として.NET層に返される。`  
    `"""`  
    `# 静的情報`  
    `character_id: str`  
    `name: str`  
    `personality: str`  
    `background: str`

    `# 動的な内的状態`  
    `values: Dict[str, float]`  
    `emotions: Dict[str, float]`  
    `desires: Dict[str, float]`

    `# 現在のアクションのコンテキスト`  
    `timeline_context: List[Dict] # 例: 最近の投稿`  
    `world_event: Optional[str]`

    `# 相互作用する他者との関係性`  
    `relationships: List[RelationshipState]`

    `# 'Think'ステップの出力（グラフ内で生成）`  
    `thought: Optional[str]`  
    `action_content: Optional[str]`

    `# .NET層に返却するためのデータベース更新命令（グラフ内で生成）`  
    `database_updates: Optional[List[Dict]]`

### **5.3. データベース更新コマンドスキーマ**

AIが生成する状態更新コマンドは、この統一JSONスキーマに従う。これにより、Python(AI)と.NET(バックエンド)間の連携を安定させる。

* **共通構造:**  
  `{`  
    `"command": "コマンド名",`  
    `"params": { /* ... パラメータ ... */ }`  
  `}`

* **定義済みコマンド:**  
  * update\_emotion: 単一の感情値を更新する。(params: {"emotion": "joy", "value": 0.8})  
  * update\_desire: 単一の欲求値を更新する。(params: {"desire": "knowledge", "value": 0.75})  
  * add\_relationship\_tag: 他キャラクターとの関係性にタグを追加する。(params: {"target\_character\_id": "some-uuid", "tag": "friend"})

## **6\. LLM連携とBYOKモデル**

* **基本方針:** LLMにはJSON形式で「思考」と「行動」を提案させ、最終的な状態更新はC\#のコードが責任を持つ。  
* **デフォルト動作:** ユーザーがAPIキー未設定の場合、アプリ側が用意したGoogle Gemini 1.5 Flashのキーを使用。利用は**1日10回**の行動に制限。  
* **ユーザーキー利用 (BYOK):** ユーザーが自身のAPIキーを設定した場合、そのキーを使用して**回数無制限**でキャラクターを動作させられる。