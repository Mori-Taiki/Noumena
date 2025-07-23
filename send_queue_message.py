import os
import json
from azure.storage.queue import QueueClient

# Azuriteの接続文字列
connect_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVEZdVliLCzZGFFzzVLQ1ZcCollapsed==;BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;TableEndpoint=http://azurite:10002/devstoreaccount1;"
queue_name = "character-action-queue"

# キュークライアントの作成
queue_client = QueueClient.from_connection_string(connect_str, queue_name)

# キューが存在しない場合は作成
queue_client.create_queue(timeout=30)

# 送信するメッセージ（CharacterStateのJSON表現）
# YOUR_CHARACTER_ID を先ほど作成したキャラクターのIDに置き換えてください
character_state_message = {
    "character_id": "ac6925af-6f29-4453-93e5-bd04fb5ce5df",
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

print(f"Message sent to queue '{queue_name}': {message_content}")
