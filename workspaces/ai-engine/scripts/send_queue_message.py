import os
import json
from azure.storage.queue import QueueClient, TextBase64EncodePolicy, TextBase64DecodePolicy

# Azuriteの接続文字列
# 環境変数 `AZURE_STORAGE_CONNECTION_STRING` から接続文字列を読み込みます。
AZURITE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not AZURITE_CONNECTION_STRING:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable must be set.")
QUEUE_NAME = "character-action-queue"

# キューサービスクライアントの作成（エンコーディングなし）
queue_client = QueueClient.from_connection_string(
    conn_str=AZURITE_CONNECTION_STRING,
    queue_name=QUEUE_NAME,
    message_encode_policy=None,
    message_decode_policy=None
)

# キューが存在しない場合は作成する
try:
    queue_client.create_queue()
    print(f"Queue '{QUEUE_NAME}' created.")
except Exception as e:
    # キューが既に存在する場合など
    print(f"Queue '{QUEUE_NAME}' already exists or an error occurred: {e}")

# 送信するメッセージ（CharacterStateのJSON表現）
character_state_message = {
    "character_id": "c1fc6abd-3cb4-4bd0-bcba-22004870e821",
    "name": "TestCharacter",
    "personality": "Curious and adventurous",
    "background": "A wanderer who seeks knowledge.",
    "values": {"knowledge": 0.9, "freedom": 0.8},
    "emotions": {"joy": 0.7, "curiosity": 0.8},
    "desires": {"explore": 0.9, "learn": 0.8},
    "timeline_context": [],
    "world_event": None,
    "relationships": []
}

# メッセージをJSON文字列に変換
message_content = json.dumps(character_state_message)

# メッセージをキューに送信
queue_client.send_message(message_content)

print(f"Message sent to queue '{QUEUE_NAME}': {message_content}")

# キューのメッセージ数を取得して表示
properties = queue_client.get_queue_properties()
print(f"Current number of messages in queue '{QUEUE_NAME}': {properties.approximate_message_count}")
