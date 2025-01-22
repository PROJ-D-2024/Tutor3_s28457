from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Example predictive model (Linear Regression)
model = LinearRegression()
X_train = np.array([[1], [2], [3], [4], [5]])
y_train = np.array([2, 4, 6, 8, 10])  # Simple 2x function
model.fit(X_train, y_train)

# Request body model
class PredictionRequest(BaseModel):
    input_value: float

@app.get("/")
def root():
    return {"message": "Welcome to the Predictive Model API!"}

@app.post("/predict/")
def predict(request: PredictionRequest):
    try:
        input_array = np.array([[request.input_value]])
        prediction = model.predict(input_array)
        return {"input": request.input_value, "prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))