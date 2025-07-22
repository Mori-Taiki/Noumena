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
    timeline_context: List[Dict] # 例: 最近の投稿
    world_event: Optional[str]

    # 相互作用する他者との関係性
    relationships: List[RelationshipState]

    # 'Think'ステップの出力（グラフ内で生成）
    thought: Optional[str]
    action_content: Optional[str]

    # .NET層に返却するためのデータベース更新命令（グラフ内で生成）
    database_updates: Optional[List[Dict]]
