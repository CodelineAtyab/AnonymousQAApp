import os
import logging
import traceback

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.logging_service import logging
from src.question_service import get_db_connection_instance


# Instantiate a logger instance to write info and error level logs
logger = logging.getLogger(os.path.basename(__file__))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

dict_of_questions = {
    "q1": "Are you happy with what's gpoing on ?",
    "q2": "Are you facing any challenges ?",
    "q3": "Are there any blockers ?"
}


@app.get(path="/api/v1/questions")
def get_all_questions():
    return_value = {"data": None, "errMsg": None}
    db_connection = get_db_connection_instance()
    try:
        logger.info("Returning all of the questions")
        return_value["data"] = {key: value for key, value in db_connection.fetch_questions()}
    except Exception:
        return_value["errMsg"] = "Unable to retrieve questions"
        logger.error(traceback.format_exc())
    finally:
        db_connection.disconnect()

    return return_value


@app.post(path="/api/v1/questions")
async def add_question(request: Request):
    return_value = {"data": None, "errMsg": None}
    recv_json_data = await request.json()
    logger.info(f"Creating a question based on {recv_json_data}")

    db_connection = get_db_connection_instance()
    try:

        for key, value in recv_json_data.items():
            db_connection.insert_question(question_id=str(key), question_text=str(value))
        return_value["data"] = recv_json_data
    except Exception:
        return_value["errMsg"] = "Unable to post the question"
        logger.error(traceback.format_exc())
        try:
            db_connection.rollback()
        except Exception:
            logger.error(traceback.format_exc())
    finally:
        db_connection.disconnect()

    return return_value


if __name__ == "__main__":
    # Run app on port 0.0.0.0, so it can receive traffic from external clients and not just localhost
    uvicorn.run(app, host="0.0.0.0", port=8080)
