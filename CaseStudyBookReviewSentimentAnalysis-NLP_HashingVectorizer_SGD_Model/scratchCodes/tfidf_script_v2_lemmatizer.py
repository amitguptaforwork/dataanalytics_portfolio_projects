import argparse
import json
import os
import sys
from typing import List, Tuple, Optional

import numpy as np
import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from joblib import Parallel, delayed

# ---------- Utility Functions ----------

import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
# run once
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download("stopwords")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def custom_lemmatize(text):
    # Lowercase
    text = text.lower()
    # Remove non-letters, tokenize
    tokens = re.findall(r"[a-z]+", text)
    # Lemmatize and filter stopwords
    return [lemmatizer.lemmatize(tok) for tok in tokens if tok not in stop_words]

def load_json_any(path: str) -> pd.DataFrame:
    """
    Loads either:
    - JSON array file
    - JSON lines (one object per line)
    Returns a pandas DataFrame.
    """
    with open(path, "r", encoding="utf-8") as f:
        first = f.read(1)
        f.seek(0)
        if first == "[":
            data = json.load(f)
            return pd.DataFrame(data)
        else:
        # json lines
            rows = [json.loads(line) for line in f if line.strip()]
            return pd.DataFrame(rows)

def concat_text(df: pd.DataFrame) -> List[str]:
    """Combine summary + reviewText into one string per review."""
    s = df["summary"]
    r = df["reviewText"] 
    return (s.fillna("").astype(str) + " " + r.fillna("").astype(str)).str.strip().tolist()


def score_to_label(overall: float) -> int:
    """
    Map overall score to label:
    0: 0 <= score < 3 (negative)
    1: 3 <= score < 4 (mixed)
    2: 4 <= score <= 5 (positive)
    """
    if overall < 3.0:
        return 0
    elif overall < 4.0:
        return 1
    else:
        return 2

# ---------- Model Builder ----------
def build_pipeline(n_features=50000, n_jobs=-1 ,loss="hinge", alpha=1e-5) -> Pipeline:
    """
    Memory‑efficient text classifier using HashingVectorizer + SGDClassifier.
    
    Args:
        n_features: feature hashing dimensionality
        loss: "hinge" for SVM-style, "log_loss" for logistic regression
        alpha: regularization strength
    """
    pipe = Pipeline(
        steps=[
            ("vect", HashingVectorizer(
                analyzer=custom_lemmatize,
                n_features=n_features,
                ngram_range=(1, 1),   
                alternate_sign=False, 
                norm="l2",
                dtype=np.float32,   # Use 32‑bit floats for internal computation
            )),
            ("clf", SGDClassifier(
            loss=loss,
            alpha=alpha,
            max_iter=1,      
            learning_rate="optimal",
            random_state=42,
            n_jobs=n_jobs,
            class_weight="balanced",
            warm_start=True,
        ))
        ]
    )   
    return pipe

# ---------- Parallel Fold Execution ----------

def run_fold(fold, train_idx, val_idx, X, y, n_features, n_jobs, loss, alpha):
    """Training + evaluation for one fold."""
    print(f"[Fold {fold}] Starting...")
    model = build_pipeline(n_features,n_jobs, loss, alpha)

    X_train = [X[i] for i in train_idx]
    y_train = y[train_idx]
    X_val = [X[i] for i in val_idx]
    y_val = y[val_idx]

    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    acc = accuracy_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred, average="weighted")
    prec = precision_score(y_val, y_pred, average="weighted")
    rec = recall_score(y_val, y_pred, average="weighted")

    print(f"[Fold {fold}] Accuracy: {acc:.4f}, F1: {f1:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}")
    return np.array([acc, f1, prec, rec])

# ---------- Main Cross-Validation Pipeline ----------

def run_crossval_pipeline(  train_path,
                            test_path,
                            write_files=False,
                            test_out="result.csv",
                            n_splits=3,
                            n_features=50000,
                            n_jobs=-1,
                            loss="hinge",
                            alpha=1e-5):
    """
    Parallel cross-validation pipeline using HashingVectorizer + SGDClassifier.
    """

    # Load data
    df_train = load_json_any(train_path)
    df_test = load_json_any(test_path)

    X = concat_text(df_train)
    y = df_train["overall"].astype(float).apply(score_to_label).values

    print(f"Loaded {len(X)} training samples.")
    print(f"Running {n_splits}-fold cross-validation on {os.cpu_count()} cores...")

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Run folds in parallel
    metrics = Parallel(n_jobs=n_jobs, verbose=10)(
        delayed(run_fold)(fold, train_idx, val_idx, X, y, n_features, n_jobs,loss, alpha)
        for fold, (train_idx, val_idx) in enumerate(kf.split(X), start=1)
    )

    metrics = np.vstack(metrics)
    print("\n========== Cross-Validation Summary ==========")
    print(f"Avg Accuracy : {metrics[:,0].mean():.4f}")
    print(f"Avg F1-score : {metrics[:,1].mean():.4f}")
    print(f"Avg Precision: {metrics[:,2].mean():.4f}")
    print(f"Avg Recall   : {metrics[:,3].mean():.4f}")
    print("==============================================\n")

    # Train final model on all data
    print("Training final model on all training data...")
    final_model = build_pipeline(n_features, n_jobs,loss, alpha)
    final_model.fit(X, y)

    # Predict test set
    X_test = concat_text(df_test)
    test_pred = final_model.predict(X_test)

    if write_files:
        pd.DataFrame({"label": test_pred.astype(int)}).to_csv(test_out, index=False)
        print(f"✅ Test predictions written to {test_out}")

    return test_pred

test_pred = run_crossval_pipeline(
    train_path="reviews_train.json",
    test_path="reviews_test.json",
    write_files=True,
    n_splits=8,
    n_features=2**15,
    n_jobs=-1,      # use all CPU cores
    loss="log_loss",   # "log_loss" for logistic regression, "hinge" for SVM
    alpha=1e-5
)