import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


filename = input("Enter the CSV file name (with .csv extension): ")
try:
    df = pd.read_csv(filename)
except Exception as e:
    print(f"Error loading file: {e}")
    exit()


df_numeric = pd.get_dummies(df)


X = df_numeric.iloc[:, :-1].values
y = df_numeric.iloc[:, -1].values

n_trees = int(input("Enter the number of decision trees for Random Forest: "))
impurity = input("Enter splitting criterion ('gini' or 'entropy'): ").strip().lower()
if impurity not in ['gini', 'entropy']:
    print("Invalid criterion, defaulting to gini")
    impurity = 'gini'

splits = [("70-30", 0.7), ("60-40", 0.6), ("75-25", 0.75)]
results = []
conf_matrices = {}

for split_name, train_size in splits:

    idx = np.arange(len(y))
    np.random.seed(42)
    np.random.shuffle(idx)

    split_point = int(train_size * len(y))
    X_train, X_test = X[idx[:split_point]], X[idx[split_point:]]
    y_train, y_test = y[idx[:split_point]], y[idx[split_point:]]


    clf = RandomForestClassifier(n_estimators=n_trees, criterion=impurity, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)


    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    results.append({
        'Split': split_name,
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1_Score': f1
    })

    print(f"\nConfusion Matrix for {split_name} split:")
    print(cm)


df_results = pd.DataFrame(results)
pd.set_option('display.float_format', "{:.4f}".format)
print("\nMetrics for each split:")
print(df_results.set_index("Split"))


best_row = df_results.loc[df_results['F1_Score'].idxmax()]
print(f"\nBest split according to F1 Score: {best_row['Split']}")
print(f"Metrics for best split:\nAccuracy: {best_row['Accuracy']:.4f}, Precision: {best_row['Precision']:.4f}, "
      f"Recall: {best_row['Recall']:.4f}, F1 Score: {best_row['F1_Score']:.4f}")
