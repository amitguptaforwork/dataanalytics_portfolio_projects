#To run the file
#streamlit run demo_streamlit.py
import streamlit as st
import pickle

model = pickle.load(open("final_model.pkl", "rb"))

st.title("Book Review Sentiment Classifier")

review = st.text_area("Enter review text:")
if st.button("Predict"):
    pred = int(model.predict([review])[0])
    label_map = {0: "Negative", 1: "Mixed", 2: "Positive"}
    st.success(f"Predicted Label: {label_map[pred]}")