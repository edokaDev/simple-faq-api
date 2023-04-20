from fastapi import FastAPI
import uvicorn

from endpoints.user_endpoints import user_router
from endpoints.auth_endpoint import auth_router
from endpoints.category_endpoints import category_router
from endpoints.question_endpoints import question_router
from endpoints.answer_endpoints import answer_router

app = FastAPI(
    title="qNyasa Q-A Bot",
    description="Questions and answer Bot",
    version="1.0",
)

@app.get('/', tags=['Welcome'])
def index():
    return 'Hello and welcome'

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(question_router)
app.include_router(answer_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
