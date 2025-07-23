import os
from azure.storage.queue import QueueClient, QueueServiceClient
from azure.core.exceptions import ClientAuthenticationError, ResourceExistsError

# Azuriteの公式ドキュメントで推奨されている、完全な形式の接続文字列
# ホスト名は必ず '127.0.0.1' を使用します
AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
)
QUEUE_NAME = "test-queue-from-script"

print("--- Azurite接続テスト開始 ---")

try:
    # 接続文字列から直接QueueClientを生成するのが最も確実
    queue_client = QueueClient.from_connection_string(
        conn_str=AZURITE_CONNECTION_STRING, 
        queue_name=QUEUE_NAME
    )

    # 1. キューが存在しない場合のみ作成する
    try:
        print(f"キュー '{QUEUE_NAME}' を作成しようとしています...")
        queue_client.create_queue()
        print(f"キュー '{QUEUE_NAME}' を作成しました。")
    except ResourceExistsError:
        print(f"キュー '{QUEUE_NAME}' は既に存在します。")
    except Exception as e:
        print(f"キュー作成中に予期せぬエラー: {e}")
        raise

    # 2. メッセージを送信する
    message = "Hello, Azurite! This is a test message."
    print(f"メッセージ '{message}' を送信しています...")
    queue_client.send_message(message)
    print("メッセージの送信に成功しました！")

    print("\n--- テスト成功！---")

except ClientAuthenticationError as e:
    print("\n--- 認証エラーが発生しました ---")
    print("エラー詳細:", e)
    print("\n考えられる原因:")
    print("1. Azuriteコンテナが起動していない、または正しくないコマンドで起動している。")
    print("2. 接続文字列のホスト名やポートが間違っている。")
    print("3. Dockerのネットワーク設定に問題がある。")

except Exception as e:
    print(f"\n--- 予期せぬエラーが発生しました ---")
    print("エラー種別:", type(e).__name__)
    print("エラー詳細:", e)