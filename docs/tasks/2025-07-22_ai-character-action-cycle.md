# タスクリスト: AI Character Action Cycle

**関連仕様:** [AI Character Action Cycle](../specs/2025-07-22_ai-character-action-cycle.md)
**関連設計:** [AI Character Action Cycle](../design/2025-07-22_ai-character-action-cycle.md)

---

## 実装タスク

1.  **[AI-Engine] Implement Azure Function queue trigger boilerplate (Issue #13)**
    -   **担当:** Coder
    -   **内容:** Azure Storage Queue (`character-action-queue`) からのメッセージをトリガーとするPython Azure Functionの基本的な雛形を作成する。
    -   **ファイル:** `workspaces/ai-engine/function_app.py`

2.  **[AI-Engine] Implement Neo4j connection logic in Python Function (Issue #15)**
    -   **担当:** Coder
    -   **内容:** 環境変数から接続情報を読み取り、Neo4jデータベースへの接続とセッション管理を行うリポジトリモジュールを作成する。
    -   **ファイル:** `workspaces/ai-engine/app/repositories/neo4j_repository.py`

3.  **[AI-Engine] Define LangGraph StateGraph with CharacterState schema (Issue #14)**
    -   **担当:** Coder
    -   **内容:** `CharacterState`を状態として使用する`langgraph.StateGraph`を初期化し、エントリーポイントとノードを登録する基本的な構造を定義する。
    -   **ファイル:** `workspaces/ai-engine/app/graph/main.py`

4.  **[AI-Engine] Implement `perceive_node` to fetch context from Neo4j (Issue #18)**
    -   **担当:** Coder
    -   **内容:** `character_id`を基にNeo4jからキャラクターの全コンテキストを取得し、`CharacterState`オブジェクトを構築する`perceive_node`を実装する。
    -   **ファイル:** `workspaces/ai-engine/app/graph/nodes/perceive.py`

5.  **[AI-Engine] Implement `think_node` with structured LLM call (Issue #19)**
    -   **担当:** Coder
    -   **内容:** `CharacterState`からプロンプトを組み立て、構造化されたJSON（思考、行動）を返すようにLLMに指示する`think_node`を実装する。
    -   **ファイル:** `workspaces/ai-engine/app/graph/nodes/think.py`

6.  **[AI-Engine] Implement `act_node` to prepare post content and DB updates (Issue #20)**
    -   **担当:** Coder
    -   **内容:** `think_node`の出力を受けて、`Post`ノードのデータと`database_updates`コマンドリストを生成する`act_node`を実装する。
    -   **ファイル:** `workspaces/ai-engine/app/graph/nodes/act.py`

7.  **[AI-Engine] Implement transactional update function (`update_db_node`) (Issue #16)**
    -   **担当:** Coder
    -   **内容:** `database_updates`リスト内のコマンドを単一トランザクションで実行する`update_db_node`を実装する。
    -   **ファイル:** `workspaces/ai-engine/app/graph/nodes/update_db.py`
