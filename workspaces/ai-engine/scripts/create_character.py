from neo4j import GraphDatabase
import uuid
import os

uri = "bolt://localhost:7687"
username = "neo4j"
password = "password1234"

def create_character(driver):
    character_id = str(uuid.uuid4())
    name = "TestCharacter"
    personality = "Curious and adventurous"
    background = "A wanderer who seeks knowledge."
    values = {"knowledge": 0.9, "freedom": 0.8}
    emotions = {"joy": 0.7, "curiosity": 0.8}
    desires = {"explore": 0.9, "learn": 0.8}

    with driver.session() as session:
        query = (
            "CREATE (c:Character {id: $character_id, name: $name, personality: $personality, background: $background, values: $values, emotions: $emotions, desires: $desires}) "
            "RETURN c"
        )
        session.run(query, character_id=character_id, name=name, personality=personality, background=background, values=values, emotions=emotions, desires=desires)
        print(f"Character {name} with ID {character_id} created successfully.")
        return character_id

if __name__ == "__main__":
    driver = GraphDatabase.driver(uri, auth=(username, password))
    new_character_id = create_character(driver)
    print(f"New character ID: {new_character_id}")
    driver.close()

if __name__ == "__main__":
    driver = GraphDatabase.driver(uri, auth=(username, password))
    create_character(driver)
    driver.close()
