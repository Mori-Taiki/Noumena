import logging
from app.graph.state import CharacterState
from app.repositories.neo4j_repository import neo4j_repository

def update_db_node(state: CharacterState) -> CharacterState:
    """Executes all database updates in a single transaction."""
    character_name = state.get("name")
    logging.info(f"---UPDATE DB: Updating database for {character_name}---")

    updates = state.get("database_updates")
    if not updates:
        logging.warning("No database updates to perform.")
        return state

    driver = neo4j_repository.get_driver()
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for update in updates:
                command = update.get("command")
                params = update.get("params")
                if command == "create_post":
                    character_id = params["character_id"]
                    content = params["content"]
                    thought = params["thought"]
                    meta_snapshot = params["meta_snapshot"]
                    # Neo4jにPostノードを作成し、Characterと関連付ける
                    query = (
                        "MATCH (c:Character {id: $character_id}) "
                        "CREATE (p:Post {id: randomUUID(), content: $content, thought: $thought, meta_snapshot: $meta_snapshot, created_at: datetime()}) "
                        "CREATE (c)-[:POSTED]->(p)"
                    )
                    tx.run(query, character_id=character_id, content=content, thought=thought, meta_snapshot=meta_snapshot)
                    logging.info(f"Created post for character {character_id}")
                else:
                    logging.warning(f"Unknown command: {command}")

    logging.info(f"---UPDATE DB: Successfully updated database for {character_name}---")
    return state
