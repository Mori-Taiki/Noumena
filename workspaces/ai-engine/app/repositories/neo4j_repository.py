import os
from neo4j import GraphDatabase

class Neo4jRepository:
    _instance = None
    _driver = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jRepository, cls).__new__(cls)
            uri = os.environ.get("NEO4J_URI")
            user = os.environ.get("NEO4J_USER")
            password = os.environ.get("NEO4J_PASSWORD")
            if not all([uri, user, password]):
                raise ValueError("NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD environment variables must be set.")
            cls._driver = GraphDatabase.driver(uri, auth=(user, password))
        return cls._instance

    def close(self):
        if self._driver is not None:
            self._driver.close()
            self.__class__._instance = None
            self.__class__._driver = None

    def get_driver(self):
        return self._driver

    def run_query(self, query: str, parameters: dict = None):
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

# シングルトンインスタンスの提供
neo4j_repository = Neo4jRepository()
