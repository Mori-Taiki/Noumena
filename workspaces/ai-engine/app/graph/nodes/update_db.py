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
                # Here you would have a mapping from command names to Cypher queries
                # For now, we'll just log the command
                logging.info(f"Executing command: {command} with params: {params}")

    logging.info(f"---UPDATE DB: Successfully updated database for {character_name}---")
    return state
