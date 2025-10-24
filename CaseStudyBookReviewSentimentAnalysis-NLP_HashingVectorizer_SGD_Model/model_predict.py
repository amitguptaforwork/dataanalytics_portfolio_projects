#USAGE GUIDE

# Uses defaults
# python model_predict.py

# # Or with custom paths
# python model_predict.py --test_file my_test.json --out_file predictions.csv --model_path final_model.pkl
import argparse
import json
import pickle
import pandas as pd
import numpy as np
import time
from typing import List
from model_train import concat_text, load_json_any  # reusing utilities

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def load_model(model_path: str):
    """Load the trained model from pickle file."""
    start = time.time()
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print(f"✅ {GREEN}Loaded model from {model_path} (Time: {time.time() - start:.2f}s)")
    return model

def predict(model, test_path: str, out_path: str):
    """Run predictions on test data, save results, and report time/size."""
    start = time.time()

    # Load and preprocess
    df_test = load_json_any(test_path)
    X_test = concat_text(df_test)
    n_samples = len(X_test)
    print(f"📄{GREEN} Loaded {n_samples} test samples from {test_path}")

    # Predict
    preds = model.predict(X_test)

    # Save output
    pd.DataFrame({"label": preds.astype(int)}).to_csv(out_path, index=False)

    elapsed = time.time() - start
    print(f"🔮 {GREEN}Predictions written to {out_path}")
    print(f"📊 {YELLOW}Processed {n_samples} inputs in {elapsed:.2f} seconds")
    print(f"⚡ {GREEN}Throughput: {n_samples / elapsed:.2f} samples/sec")
    print(f"{RESET}")

def main(test_file, out_file, model_path):

    print(f"{CYAN}Running predictions...\n Model: {model_path}\n Test file: {test_file}\n Output: {out_file}\n")

    model = load_model(model_path)
    predict(model, test_file, out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict using trained sentiment model")
    parser.add_argument("--test_file",  type=str, default="reviews_test.json",  help="Path to test JSON")
    parser.add_argument("--out_file",   type=str, default="result.csv",         help="Output CSV file path")
    parser.add_argument("--model_path", type=str, default="final_model.pkl", help="Path to trained model pickle file")
    args = parser.parse_args()

    main(test_file=args.test_file, out_file=args.out_file, model_path=args.model_path)