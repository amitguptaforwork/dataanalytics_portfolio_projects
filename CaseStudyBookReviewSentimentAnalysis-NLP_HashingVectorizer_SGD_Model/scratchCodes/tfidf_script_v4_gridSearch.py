# pip install memory-profiler
import json
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from memory_profiler import memory_usage

# ---------- Utility Functions ----------

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


def concat_text(df: pd.DataFrame):
    """Combine summary + reviewText into one string per review."""
    s = df["summary"]
    r = df["reviewText"]
    return (s.fillna("").astype(str) + " " + r.fillna("").astype(str)).str.strip()


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


# ---------- CRITICAL: Build Pipeline WITHOUT hardcoded parameters ----------
# GridSearchCV will inject parameters automatically using the param_grid

def build_pipeline() -> Pipeline:
    """
    Build pipeline with DEFAULT parameters.
    GridSearchCV will OVERRIDE these with values from param_grid.
    
    KEY INSIGHT: You don't pass parameters here!
    GridSearchCV handles that automatically.
    """
    pipe = Pipeline(
        steps=[
            ("vect", HashingVectorizer(
                # Parameters that GridSearchCV will override:
                n_features=50000,        # Will be overridden by vect__n_features
                ngram_range=(1, 1),      # Will be overridden by vect__ngram_range
                
                # Fixed parameters (not in param_grid):
                lowercase=True,
                strip_accents="unicode",
                stop_words='english',
                alternate_sign=False,
                norm="l2",
                dtype=np.float32,
            )),
            ("clf", SGDClassifier(
                # Parameters that GridSearchCV will override:
                loss="hinge",            # Will be overridden by clf__loss
                alpha=1e-5,              # Will be overridden by clf__alpha
                max_iter=10,             # Will be overridden by clf__max_iter
                
                # Fixed parameters (not in param_grid):
                early_stopping=True,
                n_iter_no_change=3,
                learning_rate="optimal",
                random_state=42,
                n_jobs=-1,
                class_weight="balanced",
                warm_start=True,
            ))
        ]
    )
    return pipe


# ---------- GridSearchCV Pipeline ----------

def run_gridsearch_pipeline(train_path,
                            test_path,
                            write_files=False,
                            test_out="result.csv",
                            cv=3):
    """
    GridSearchCV pipeline - automatically tries all parameter combinations.
    
    HOW IT WORKS:
    1. You define param_grid with parameter names like "clf__alpha"
    2. GridSearchCV creates the pipeline using build_pipeline()
    3. GridSearchCV automatically sets clf.alpha = value from param_grid
    4. It does this for EVERY combination and finds the best one
    """

    # Load data
    df_train = load_json_any(train_path)
    df_test = load_json_any(test_path)

    X = concat_text(df_train)
    y = df_train["overall"].astype(float).apply(score_to_label).values

    print(f"Loaded {len(X)} training samples.")
    
    # ============================================
    # KEY PART: Define parameter grid
    # ============================================
    # Format: "step_name__parameter_name": [values to try]
    # "vect__" refers to the HashingVectorizer step
    # "clf__" refers to the SGDClassifier step
    
    param_grid = {
        # HashingVectorizer parameters
        "vect__n_features": [2**14, 2**15, 2**16],  # Try 16k, 32k, 64k features
        "vect__ngram_range": [(1, 1), (1, 2)],       # Unigrams vs unigrams+bigrams
        
        # SGDClassifier parameters
        "clf__loss": ["hinge", "log_loss"],          # SVM vs Logistic Regression
        "clf__alpha": [1e-6, 1e-5, 1e-4],            # Regularization strength
        "clf__max_iter": [10, 20, 30],               # Training iterations
    }
    
    # Total combinations: 3 * 2 * 2 * 3 * 3 = 108 models to try!
    
    print(f"\nGridSearchCV will try {np.prod([len(v) for v in param_grid.values()])} combinations")
    print(f"With {cv}-fold cross-validation = {np.prod([len(v) for v in param_grid.values()]) * cv} total fits")
    print("This may take a while...\n")

    # ============================================
    # Create GridSearchCV object
    # ============================================
    grid_search = GridSearchCV(
        estimator=build_pipeline(),      # The pipeline to optimize
        param_grid=param_grid,            # Parameter combinations to try
        cv=cv,                            # Number of cross-validation folds
        scoring='f1_weighted',            # Metric to optimize
        n_jobs=-1,                        # Use all CPU cores
        verbose=2,                        # Show progress
        return_train_score=True           # Track training scores too
    )

    # ============================================
    # Fit GridSearchCV - this does ALL the work!
    # ============================================
    print("Starting GridSearchCV...")
    grid_search.fit(X, y)
    
    # ============================================
    # Results
    # ============================================
    print("\n" + "="*60)
    print("GRIDSEARCH COMPLETED!")
    print("="*60)
    print(f"\n🏆 Best Parameters Found:")
    for param, value in grid_search.best_params_.items():
        print(f"   {param}: {value}")
    
    print(f"\n📊 Best Cross-Validation F1 Score: {grid_search.best_score_:.4f}")
    
    # The best model is automatically retrained on ALL data
    best_model = grid_search.best_estimator_
    
    # Show detailed metrics on training data
    y_train_pred = best_model.predict(X)
    print(f"\n📈 Training Set Performance (with best params):")
    print(f"   Accuracy : {accuracy_score(y, y_train_pred):.4f}")
    print(f"   F1-score : {f1_score(y, y_train_pred, average='weighted'):.4f}")
    print(f"   Precision: {precision_score(y, y_train_pred, average='weighted'):.4f}")
    print(f"   Recall   : {recall_score(y, y_train_pred, average='weighted'):.4f}")

    # ============================================
    # Predict on test set
    # ============================================
    X_test = concat_text(df_test)
    test_pred = best_model.predict(X_test)

    if write_files:
        pd.DataFrame({"label": test_pred.astype(int)}).to_csv(test_out, index=False)
        print(f"\n✅ Test predictions written to {test_out}")

    # ============================================
    # Show top 5 parameter combinations
    # ============================================
    results_df = pd.DataFrame(grid_search.cv_results_)
    results_df = results_df.sort_values('rank_test_score')
    
    print("\n" + "="*60)
    print("TOP 5 PARAMETER COMBINATIONS")
    print("="*60)
    for idx, row in results_df.head(5).iterrows():
        print(f"\nRank {int(row['rank_test_score'])}:")
        print(f"  F1 Score: {row['mean_test_score']:.4f} (+/- {row['std_test_score']:.4f})")
        print(f"  Parameters: {row['params']}")

    return {
        "best_params": grid_search.best_params_,
        "best_cv_f1": f"{grid_search.best_score_:.4f}",
        "best_model": best_model,
        "all_results": results_df
    }


def train():
    start = time.time()
    
    results = run_gridsearch_pipeline(
        train_path="reviews_train.json",
        test_path="reviews_test.json",
        write_files=True,
        test_out="result_gridsearch.csv",
        cv=3  # Reduced from 8 for faster execution
    )
    
    print(f"\n\033[92m✅ Training Complete!")
    print(f"\033[93m⏱️  Time: {time.time() - start:.2f} seconds")
    
    return results


if __name__ == "__main__":
    mem_usage = memory_usage((train,))
    print(f"\033[93m💾 Peak Memory usage: {max(mem_usage):.1f} MB")