import logging
from app.graph.state import CharacterState
from app.repositories.neo4j_repository import neo4j_repository

def perceive_node(state: CharacterState) -> CharacterState:
    """Fetches the character's full context from Neo4j."""
    character_id = state.get("character_id")
    logging.info(f"---PERCEIVE: Fetching data for {character_id}---")

    # This is a placeholder. In a real implementation, you would fetch
    # this data from Neo4j using the repository.
    # For now, we'll just populate it with some dummy data.
    dummy_state: CharacterState = {
        "character_id": character_id,
        "name": "Elias Vance",
        "personality": "A stoic, yet curious historian.",
        "background": "Born in a city of scholars, Elias has dedicated his life to uncovering lost histories.",
        "values": {"knowledge": 0.9, "tradition": 0.7},
        "emotions": {"joy": 0.3, "sadness": 0.5, "curiosity": 0.8},
        "desires": {"discovery": 0.9, "peace": 0.6},
        "timeline_context": [
            {"content": "The old library is quieter than usual today."}
        ],
        "world_event": None,
        "relationships": [],
        "thought": None,
        "action_content": None,
        "database_updates": None
    }

    logging.info(f"---PERCEIVE: Successfully fetched data for {character_id}---")
    return dummy_state
