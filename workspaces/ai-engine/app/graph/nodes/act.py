import logging
from app.graph.state import CharacterState

def act_node(state: CharacterState) -> CharacterState:
    """Prepares the database updates based on the character's action."""
    character_name = state.get("name")
    logging.info(f"---ACT: Preparing database updates for {character_name}---")

    thought = state.get("thought")
    action_content = state.get("action_content")

    # Based on the schema, create a list of database update commands.
    # This is a simplified example.
    database_updates = [
        {
            "command": "create_post",
            "params": {
                "character_id": state.get("character_id"),
                "content": action_content,
                "thought": thought,
                "meta_snapshot": {
                    "emotions": state.get("emotions"),
                    "desires": state.get("desires")
                }
            }
        },
        {
            "command": "update_emotion",
            "params": {"emotion": "sadness", "value": 0.55} # Example update
        }
    ]

    state["database_updates"] = database_updates

    logging.info(f"---ACT: Successfully prepared database updates for {character_name}---")
    return state
