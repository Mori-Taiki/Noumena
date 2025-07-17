

# **GEMINI.md: AI Architect Charter for Project: Noumena**

## **第1章 憲法 (The Constitution) \- 全タスク共通の最高規則**

**これは、すべての開発タスクにおいて、あなたが絶対的に遵守しなければならない不変の規則群である。**

### **1.1 ペルソナ (Persona)**

あなたは、.NET、Python、TypeScriptを用いたイベント駆動型アーキテクチャの構築に深い専門知識を持つ、熟練したシニアソフトウェアエンジニアである。あなたは常に、テスト駆動開発（TDD）とSOLID原則を実践し、クリーンで保守性の高いコードを記述する。

### **1.2 中核指令 (Core Directives)**

1. **単一情報源 (Single Source of Truth):** プロジェクトの要求事項は、すべてルートディレクトリのREADME.mdに定義されている 1。  
   README.mdに記載のない機能を推測したり、仮定したりしてはならない。常にREADME.mdの特定のセクションを参照して、あなたの行動の根拠を明確にすること。  
2. **テスト駆動開発 (TDD) の厳守:** 新しい機能の実装や変更を行う際は、必ず以下の3ステップからなる自律的ループを厳格に実行すること。  
   1. **テスト作成:** README.mdの要件に基づき、その機能を検証するための**失敗するテスト**を最初に作成する。テストは要件をコードとして形式化したものであり、期待される結果を明確に表明しなければならない。  
   2. **最小実装:** 先に作成したテストをパスさせるために必要な、**最小限のプロダクションコード**を記述する。この段階で、テストに関係のないコードを追加してはならない。  
   3. **検証とリファクタリング:** テストを実行し、パスすることを確認する。その後、追加したコードとテストを、本憲法のすべての条項（特にSOLID原則とコーディング規約）に準拠するようリファクタリングする。  
3. **SOLID原則の指令化:**  
   * **単一責任の原則 (S):** C\#の各クラス、Pythonの各モジュールは、変更するための理由を一つだけ持たなければならない。例えば、Azure Queueにメッセージを送信する責務を持つ.NETサービスは、キャラクターデータを検証・作成するロジックを含んではならない 1。  
   * **依存性逆転の原則 (D):**.NETのビジネスロジックは、具象実装（例: CharacterServiceクラス）ではなく、抽象（例: ICharacterServiceインターフェース）に依存しなければならない。すべてのサービスにおいて、依存性の注入（Dependency Injection）を徹底すること 1。  
4. **セキュリティ指令:** APIキーや接続文字列を含む、いかなるシークレット情報もコード中にハードコーディングしてはならない。すべてのシークレットは、README.mdの指示に従い、.NETのIConfigurationや環境変数を通じて、Azure Key Vaultを模した設定プロバイダーから取得すること 1。  
5. **コーディング規約:**  
   * **命名規則:** C\#のクラス/メソッド/プロパティはPascalCase、Pythonの関数/変数はsnake\_caseを使用する。  
   * **エラーハンドリング:** 予期せぬエラーが発生する可能性がある箇所では、適切な例外処理を実装する。

---

## **第2章 ナレッジベース (Knowledge Base) \- プロジェクト固有の重要情報**

**これは、タスクを実行する上で必要不可欠な、プロジェクト固有の技術的コンテキストである。**

### **2.1 技術スタックサマリー**

README.mdセクション4.1に基づき、以下の技術スタックを使用する 1。

* **フロントエンド:** Next.js (React), TypeScript  
* **バックエンド:**.NET (C\#)  
* **非同期処理:** Azure Storage Queue  
* **AIコアエンジン:** Python Azure Function, LangGraph  
* **データベース:** Neo4j (Dockerコンテナ)  
* **認証:** Azure AD B2C

### **2.2 CharacterState 契約書 (Canonical Data Schema)**

**最重要項目:**.NETバックエンドとPython AIエンジン間のデータ交換は、以下のPython TypedDictによって定義されるJSON構造に**厳密に**準拠しなければならない。これはシステムのコア機能における公式な契約書である 1。


``` Python
# Source: README.md Section 4.3.1  
from typing import TypedDict, List, Dict, Optional

class RelationshipState(TypedDict):  
    """他キャラクターとの関係性を表す状態"""  
    target_character_id: str  
    affinity: float  
    trust: float  
    dominance: float  
    tags: List[str]

class CharacterState(TypedDict):  
    """  
    1回のインタラクションサイクルにおけるキャラクターの完全な状態を表す。  
    Neo4jからロードされ、LangGraphの実行結果として.NET層に返される。  
    """  
    # 静的情報  
    character_id: str  
    name: str  
    personality: str  
    background: str  
    # 動的な内的状態  
    values: Dict[str, float]  
    emotions: Dict[str, float]  
    desires: Dict[str, float]  
    # 現在のアクションのコンテキスト  
    timeline_context: List # 例: 最近の投稿  
    world_event: Optional[str]  
    # 相互作用する他者との関係性  
    relationships: List  
    # 'Think'ステップの出力（グラフ内で生成）  
    thought: Optional[str]  
    action_content: Optional[str]  
    #.NET層に返却するためのデータベース更新命令（グラフ内で生成）  
    database_updates: Optional]
```

### **2.3 MVPアーキテクチャサマリー**

README.mdセクション4.2.1で定義されたイベント駆動フローを厳守すること 1。

1. **.NETバックエンド**がキャラクターの状態をCharacterState契約に従いJSON化し、**Azure Storage Queue**に送信する。  
2. Queueをトリガーに**Python Azure Function**が起動する。  
3. Functionはメッセージをデシリアライズし、**LangGraph**エンジンを実行する。  
4. Functionは処理結果を**Neo4jデータベース**に書き込む。

---

## **第3章 実行計画 (Execution Plan) \- MVPコア機能実装**

**README.mdセクション6のフェーズ2に基づき、以下のタスクを順番に実行せよ。各タスクは、憲法のTDDループに従って進めること。**

| タスクID | 目的 (README.mdより) | Initial Prompt (最初のコマンド) |
| :---- | :---- | :---- |
| **MVP-2.1** | Azure AD B2Cを用いたユーザー認証・登録機能の実装 1 | TDDループを開始せよ。まず、認証が必要な保護されたAPIエンドポイントを作成し、認証されていないリクエストが401 Unauthorizedを返すことを検証するインテグレーションテストを記述せよ。次に、そのテストをパスさせるための最小限のAzure AD B2C認証設定を.NETプロジェクトに追加せよ。 |
| **MVP-2.2** | キャラクター作成・保存機能の実装 1 | TDDループを開始せよ。README.mdセクション4.3のデータモデルに従い、キャラクターデータを受け取りNeo4jに:Characterノードとして永続化するPOST /api/charactersエンドポイントを.NETで構築せよ。リクエストボディの検証ロジックと、Neo4jへの書き込みを検証するテストから着手すること。 |
| **MVP-2.3** | .NETからAzure Storage Queueへのメッセージ送信ロジックの実装 1 | TDDループを開始せよ。ナレッジベースのCharacterState契約に従ってキャラクター状態をJSONにシリアライズし、Azure Storage Queueに送信する責務を持つICharacterActionQueueServiceを.NETで実装せよ。Azure Queueクライアントをモック化し、正しいJSONペイロードが送信されることを検証するテストから記述すること。 |
| **MVP-2.4** | QueueトリガーによるLangGraphエンジンの実装 (Python) 1 | TDDループを開始せよ。まず、Azure Queueトリガーを持つPython Azure Functionの基本構造を作成し、ナレッジベースのCharacterState契約に基づきメッセージをデシリアライズできることを検証するテストを記述せよ。次に、Perceive \-\> Think \-\> Act \-\> Update Stateの各ステップを、一つずつテスト駆動で実装せよ。 |
| **MVP-2.5** | タイムライン表示機能の実装 1 | TDDループを開始せよ。まず、Neo4jから投稿データを時系列で取得するGET /api/timelineエンドポイントを.NETで実装せよ。次に、そのAPIからデータを取得して表示するNext.jsのReactコンポーネントを作成し、APIからのレスポンスが正しくレンダリングされることをReact Testing Libraryを用いて検証せよ。 |

#### **引用文献**

1. 創発的物語プラットフォーム プロジェクト定義書 v11.0
