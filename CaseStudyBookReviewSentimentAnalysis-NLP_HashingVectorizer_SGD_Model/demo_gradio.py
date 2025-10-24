#python demo_gradio.py

import pickle
import gradio as gr

# Load your full pipeline
model = pickle.load(open("final_model.pkl", "rb"))

def predict_sentiment(review):
    pred = int(model.predict([review])[0])
    label_map = {0: "Negative", 1: "Mixed", 2: "Positive"}
    return label_map.get(pred, "Unknown")

gr.Interface(
    fn=predict_sentiment,
    inputs=gr.Textbox(label="Enter your review"),
    outputs="text",
    title="Book Review Sentiment Classifier"
).launch()