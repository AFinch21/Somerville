from fastapi import FastAPI
from model.Model import ResponseModel, EvaluationModel
from database.Database import get_db

app = FastAPI()

db = get_db()

# agent_data = get_agents(db)

# agent_pod = iniatialise_agents(agent_data)

@app.get("/get_response", response_model=ResponseModel)
async def get_response():
    """
    Endpoint to get a basic response message.
    """
    response = {
        "message": "This is your response!",
        "status": "Success"
    }
    return response

@app.get("/get_evaluation", response_model=EvaluationModel)
async def get_evaluation():
    """
    Endpoint to get an evaluation.
    """
    evaluation = {
        "score": 85,
        "feedback": "Good job! Keep it up!"
    }
    return evaluation

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)