import azure.functions as func
import logging
import json
import traceback
from app.graph.main import app as graph_app

app = func.FunctionApp()

@app.queue_trigger(arg_name="req", queue_name="character-action-queue",
                  connection="AzureWebJobsStorage")
def character_action_trigger(req: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a queue item.')

    try:
        message_body = req.get_body().decode('utf-8')
        data = json.loads(message_body)
        character_id = data.get("character_id")

        if not character_id:
            logging.error("character_id not found in the queue message.")
            return

        logging.info(f"Invoking graph for character_id: {character_id}")

        # Prepare the initial state
        initial_state = {"character_id": character_id}

        # Invoke the graph
        graph_app.invoke(initial_state)

        logging.info(f"Successfully processed character_id: {character_id}")

    except json.JSONDecodeError:
        logging.error("Error decoding JSON from queue message.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.error(traceback.format_exc())