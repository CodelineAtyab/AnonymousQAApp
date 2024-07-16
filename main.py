import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


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
    return dict_of_questions


@app.post(path="/api/v1/questions")
async def add_question(request: Request):
    recv_json_data = await request.json()
    dict_of_questions.update(recv_json_data)
    return dict_of_questions




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
