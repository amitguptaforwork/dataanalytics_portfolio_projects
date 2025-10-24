# USAGE GUIDE
# Uses default reviews_train.json
# python model_train.py

# Or specify file
# python model_train.py --train_file mydata.json    


import argparse
import json
import os
import sys
import time
import pickle
from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from joblib import Parallel, delayed
from memory_profiler import memory_usage

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve
from sklearn.preprocessing import label_binarize

# ---------- Utility Functions ----------
# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def load_json_any(path: str) -> pd.DataFrame:
    print(f"{CYAN}Reading {path}")
    with open(path, "r", encoding="utf-8") as f:
        first = f.read(1)
        f.seek(0)
        if first == "[":
            data = json.load(f)
            return pd.DataFrame(data)
        else:
            rows = [json.loads(line) for line in f if line.strip()]
            return pd.DataFrame(rows)

def concat_text(df: pd.DataFrame) -> List[str]:
    s = df["summary"]
    r = df["reviewText"]
    return (s.fillna("").astype(str) + " " + r.fillna("").astype(str)).str.strip().tolist()

def score_to_label(overall: float) -> int:
    if overall < 3.0:
        return 0
    elif overall < 4.0:
        return 1
    else:
        return 2


def plot_roc_pr_curves(model, X_val, y_val, n_classes=3, prefix=""):
    """
    Plot ROC and Precision–Recall curves for multi-class classification.
    """
    # Binarize labels for multi-class one-vs-rest
    y_true_bin = label_binarize(y_val, classes=list(range(n_classes)))

    # Get decision_function or predict_proba
    # SGDClassifier does not provide predict_proba() if we use hinge
    # SGDClassifier provides predict_proba() if we use log_loss
    if hasattr(model, "decision_function"):
        y_score = model.decision_function(X_val)
    elif hasattr(model, "predict_proba"):
        y_score = model.predict_proba(X_val)
    else:
        raise ValueError("Model does not have decision_function or predict_proba.")

    # ROC and PR
    fpr, tpr, roc_auc = {}, {}, {}
    precision, recall, pr_auc = {}, {}, {}

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_score[:, i])
        precision[i], recall[i], _ = precision_recall_curve(y_true_bin[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
        pr_auc[i] = auc(recall[i], precision[i])

    # Plot ROC curves
    plt.figure(figsize=(8, 6))
    for i in range(n_classes):
        plt.plot(fpr[i], tpr[i], label=f"Class {i} (AUC={roc_auc[i]:.2f})")
    plt.plot([0, 1], [0, 1], "k--")
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{prefix}roc_curve.png")
    plt.close()

    # Plot PR curves
    plt.figure(figsize=(8, 6))
    for i in range(n_classes):
        plt.plot(recall[i], precision[i], label=f"Class {i} (AUC={pr_auc[i]:.2f})")
    plt.title("Precision–Recall Curve")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{prefix}pr_curve.png")
    plt.close()

    print(f"✅ ROC and PR curves saved as '{prefix}roc_curve.png' and '{prefix}pr_curve.png'")

# ---------- Model Builder ----------

def build_pipeline(n_features=50000, n_jobs=-1, loss="hinge", alpha=1e-5) -> Pipeline:
    pipe = Pipeline(
        steps=[
            ("vect", HashingVectorizer(
                n_features=n_features,
                lowercase=True,
                strip_accents="unicode",
                ngram_range=(1, 2),
                stop_words='english',
                alternate_sign=False,
                norm="l2",
                dtype=np.float32,
            )),
            ("clf", SGDClassifier(
                loss=loss,
                alpha=alpha,
                max_iter=10,
                early_stopping=True,
                n_iter_no_change=3,
                learning_rate="optimal",
                random_state=42,
                n_jobs=n_jobs,
                class_weight="balanced",
                warm_start=True,
            )),
        ]
    )
    return pipe

# ---------- Parallel Fold Execution ----------

def run_fold(fold, train_idx, val_idx, X, y, n_features, n_jobs, loss, alpha):
    print(f"[Fold {fold}] Starting...")
    model = build_pipeline(n_features, n_jobs, loss, alpha)
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

# ---------- Training Function ----------

def run_training_pipeline(train_path, n_splits=3, n_features=2**16, n_jobs=-1, loss="hinge", alpha=1e-5, model_out="final_model.pkl"):
    df_train = load_json_any(train_path)
    X = concat_text(df_train)
    y = df_train["overall"].astype(float).apply(score_to_label).values

    print(f"{CYAN}Loaded {len(X)} training samples.")
    print(f"{CYAN}Running {n_splits}-fold cross-validation...")

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    metrics = Parallel(n_jobs=n_jobs, verbose=10)(
        delayed(run_fold)(fold, train_idx, val_idx, X, y, n_features, n_jobs, loss, alpha)
        for fold, (train_idx, val_idx) in enumerate(kf.split(X), start=1)
    )

    metrics = np.vstack(metrics)
    print("\n========== Cross-Validation Summary ==========")
    print(f"Avg Accuracy : {metrics[:,0].mean():.4f}")
    print(f"Avg F1-score : {metrics[:,1].mean():.4f}")
    print(f"Avg Precision: {metrics[:,2].mean():.4f}")
    print(f"Avg Recall   : {metrics[:,3].mean():.4f}")
    print("==============================================\n")

    print("Training final model on all data...")
    final_model = build_pipeline(n_features, n_jobs, loss, alpha)
    final_model.fit(X, y)
    
    #Plot and save ROC and PR curves
    plot_roc_pr_curves(final_model, X, y, n_classes=3, prefix="final_")
    # Save model to pickle
    with open(model_out, "wb") as f:
        pickle.dump(final_model, f)
    print(f"✅{GREEN}Model saved to {model_out}")

    return model_out

# ---------- Entrypoint ----------

def train(train_file):
    start = time.time()
    model_path = run_training_pipeline(train_path=train_file)
    print(f"✅{YELLOW}Training completed in {time.time()-start:.2f}s. Model: {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train sentiment model")
    parser.add_argument("--train_file", type=str, default="reviews_train.json", help="Path to training JSON file")
    args = parser.parse_args()

    mem_usage = memory_usage((train, (args.train_file,)))
    print(f"{YELLOW}Peak Memory usage: {max(mem_usage):.1f} MB")
    print(f"{RESET}")

