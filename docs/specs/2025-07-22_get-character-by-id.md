# 仕様書: 特定キャラクター取得API

## 1. 概要 (Overview)

IDで指定された単一のキャラクター情報を取得するためのAPIエンドポイントを提供する。これにより、クライアントアプリケーションは特定のキャラクターの詳細情報を表示できるようになる。

## 2. ユーザーストーリー (User Stories)

- **US-1:** APIクライアントとして、特定のキャラクターIDを指定して、そのキャラクターの完全な情報をJSON形式で取得したい。なぜなら、ユーザーにキャラクターの詳細プロフィールを表示するためだ。

## 3. 受け入れ基準 (Acceptance Criteria)

### US-1に対する受け入れ基準

- **シナリオ1:** 存在するキャラクターIDを指定して取得
    - **Given:** システムにID `char-123` を持つキャラクターが登録されている
    - **When:** APIクライアントが `GET /api/characters/char-123` をリクエストする
    - **Then:** ステータスコード200 (OK) が返却される
    - **And:** レスポンスボディには、ID `char-123` のキャラクター情報がJSON形式で含まれている

- **シナリオ2:** 存在しないキャラクターIDを指定して取得
    - **Given:** システムにID `char-999` を持つキャラクターは登録されていない
    - **When:** APIクライアントが `GET /api/characters/char-999` をリクエストする
    - **Then:** ステータスコード404 (Not Found) が返却される

## 4. スコープ外 (Out of Scope)

- 認証および認可
- 複数のキャラクターを一覧で取得する機能
- キャラクター情報の更新・削除機能
