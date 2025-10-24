import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from typing import List


# ---------- Utility Functions ----------

def score_to_label(score: float) -> int:
    """Convert numeric rating (0–5) to sentiment class."""
    if score < 3:
        return 0
    elif score < 4:
        return 1
    else:
        return 2


def load_json_any(path: str) -> pd.DataFrame:
    """Loads either a JSON array or JSON lines file."""
    import json
    with open(path, "r", encoding="utf-8") as f:
        first = f.read(1)
        f.seek(0)
        if first == "[":
            data = json.load(f)
            return pd.DataFrame(data)
        else:
            rows = [json.loads(line) for line in f if line.strip()]
            return pd.DataFrame(rows)


class ReviewDataset(Dataset):
    """PyTorch Dataset for tokenized text + labels."""
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length=256):
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=max_length
        )
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item


# ---------- Main Pipeline ----------

def run_bert_crossval_pipeline(train_path,
                               test_path,
                               write_files=False,
                               test_out="result.csv",
                               model_name="distilbert-base-uncased",
                               epochs=2,
                               batch_size=8,
                               n_splits=3):
    """
    1. Loads train & test data.
    2. Performs K-Fold cross-validation on train data (prints metrics).
    3. Optionally refits on full train and predicts test.
    """

    # --- Load Data ---
    df_train = load_json_any(train_path)
    df_test = load_json_any(test_path)

    def concat_text(df):
        s = df["summary"].fillna("") if "summary" in df.columns else ""
        r = df["reviewText"].fillna("") if "reviewText" in df.columns else ""
        return (s.astype(str) + " " + r.astype(str)).str.strip().tolist()

    X = concat_text(df_train)
    y = df_train["overall"].astype(float).apply(score_to_label).tolist()

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running on {device.upper()}")

    # --- Cross-Validation ---
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    all_metrics = []

    fold = 1
    for train_idx, val_idx in kf.split(X):
        print(f"\n==== Fold {fold}/{n_splits} ====")
        X_train = [X[i] for i in train_idx]
        y_train = [y[i] for i in train_idx]
        X_val = [X[i] for i in val_idx]
        y_val = [y[i] for i in val_idx]

        train_ds = ReviewDataset(X_train, y_train, tokenizer)
        val_ds = ReviewDataset(X_val, y_val, tokenizer)

        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

        training_args = TrainingArguments(
            output_dir=f"./bert-fold{fold}",
            save_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=epochs,
            weight_decay=0.01,
            logging_dir=f"./bert-logs-fold{fold}",
            logging_steps=50,
            report_to="none"
        )
        #Trainer automates the whole training pipeline- data loading, optimizer steps, logging and evaluation
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            tokenizer=tokenizer
        )

        trainer.train()
        #Predict on the validation set
        preds = trainer.predict(val_ds)
        y_pred = np.argmax(preds.predictions, axis=1)

        #Compute metrics
        acc = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred, average="weighted")
        prec = precision_score(y_val, y_pred, average="weighted")
        rec = recall_score(y_val, y_pred, average="weighted")

        print(f"Fold {fold} → Accuracy: {acc:.4f}, F1: {f1:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}")
        all_metrics.append([acc, f1, prec, rec])
        fold += 1

    # --- Aggregate metrics ---
    all_metrics = np.array(all_metrics)
    print("\n========== Cross-Validation Summary ==========")
    print(f"Avg Accuracy : {all_metrics[:,0].mean():.4f}")
    print(f"Avg F1-score : {all_metrics[:,1].mean():.4f}")
    print(f"Avg Precision: {all_metrics[:,2].mean():.4f}")
    print(f"Avg Recall   : {all_metrics[:,3].mean():.4f}")
    print("==============================================\n")

    # --- Final training on all data + test prediction ---
    X_test = concat_text(df_test)
    test_ds = ReviewDataset(X_test, [0]*len(df_test), tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
    full_ds = ReviewDataset(X, y, tokenizer)

    training_args = TrainingArguments(
        output_dir="./bert-full",
        per_device_train_batch_size=batch_size,
        num_train_epochs=epochs,
        learning_rate=2e-5,
        logging_dir="./bert-logs-full",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=full_ds,
        tokenizer=tokenizer
    )

    print("\n---- Training final model on all data ----")
    trainer.train()

    preds = trainer.predict(test_ds)
    test_pred = np.argmax(preds.predictions, axis=1)

    if write_files:
        pd.DataFrame({"label": test_pred.astype(int)}).to_csv(test_out, index=False)
        print(f"\n✅ Test predictions written to {test_out}")

    return test_pred

train_path='/content/drive/MyDrive/Colab Notebooks/xreviews_train.json'
test_path='/content/drive/MyDrive/Colab Notebooks/xreviews_test.json'

train_path='xreviews_train.json'
test_path='xreviews_test.json'

run_bert_crossval_pipeline(train_path=train_path,test_path=test_path)

