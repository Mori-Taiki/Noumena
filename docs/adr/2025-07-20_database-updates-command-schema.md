# ADR: AI生成データの統一更新コマンドスキーマ

- **Status**: Proposed
- **Date**: 2025-07-20

## Context

Pythonで実装されたAIエンジンがキャラクターの状態を変化させた結果を、.NETで実装されたバックエンドシステムが受け取り、永続化（データベースへの保存）を行う必要がある。この二つの異なる技術スタック間で、安定したデータ連携を実現するための統一された契約（インターフェース）が求められる。

## Decision

AIが生成する状態更新命令は、以下の統一されたJSONスキーマに従うこととする。

- **共通構造**:
  ```json
  {
    "command": "コマンド名",
    "params": { /* ... パラメータ ... */ }
  }
  ```

- **定義済みコマンド**:
  1.  **`update_emotion` (感情更新)**
      - **説明**: 単一の感情値を更新する。
      - **スキーマ**: `{"command": "update_emotion", "params": {"emotion": "joy", "value": 0.8}}`

  2.  **`update_desire` (欲求更新)**
      - **説明**: 単一の欲求値を更新する。
      - **スキーマ**: `{"command": "update_desire", "params": {"desire": "knowledge", "value": 0.75}}`

  3.  **`add_relationship_tag` (関係性タグ追加)**
      - **説明**: 他キャラクターとの関係性にタグを追加する。
      - **スキーマ**: `{"command": "add_relationship_tag", "params": {"target_character_id": "some-uuid", "tag": "friend"}}`

## Consequences

- **Positive**:
    - Python(AI)と.NET(バックエンド)の結合度が下がり、それぞれを独立して開発・変更しやすくなる。
    - コマンドスキーマが明確であるため、開発者間のコミュニケーションコストが削減される。
    - 将来的に新しい種類の状態更新を追加する際も、既存の構造に従うだけで良いため拡張性が高い。
- **Negative**:
    - AIが生成するJSONがスキーマに準拠していることを保証するためのバリデーション処理が、.NET側で必要になる。
    - AIの思考の自由度が、定義済みのコマンドセットにわずかに制約される可能性がある。
