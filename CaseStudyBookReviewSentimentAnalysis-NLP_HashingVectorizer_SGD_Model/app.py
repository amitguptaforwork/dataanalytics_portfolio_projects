#uvicorn app:app --host 0.0.0.0 --port 8000 --reload
from fastapi import FastAPI
from pydantic import BaseModel
import pickle

# Load full pipeline
model = pickle.load(open("final_model.pkl", "rb"))

# Define data schema
class Review(BaseModel):
    review: str

app = FastAPI(title="Book Review Sentiment Classifier")

@app.get("/")
def home():
    return {"message": "Book Review Sentiment Classifier API"}

@app.post("/predict")
def predict_sentiment(data: Review):
    prediction = int(model.predict([data.review])[0])
    return {"label": prediction}