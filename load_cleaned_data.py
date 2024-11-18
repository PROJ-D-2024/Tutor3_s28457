from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score


def fetch_data():
    client = MongoClient("mongodb://localhost:27017")
    db = client["thesis_project"]
    collection = db["sample_data"]
    data = pd.DataFrame(list(collection.find()))
    data.drop(columns=['_id'], inplace=True)
    return data


if __name__ == "__main__":
    data = fetch_data()
    datetime_columns = data.select_dtypes(include=['datetime64']).columns
    for col in datetime_columns:
        data[col] = (data[col] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    data = data.drop(columns=['name', 'email', 'location'], errors='ignore')
    data['category'] = data['category'].fillna('unknown')
    target_column = "category"
    label_encoder = LabelEncoder()
    data[target_column] = label_encoder.fit_transform(data[target_column])
    X = data.drop(columns=[target_column])
    y = data[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_resampled)
    X_test_scaled = scaler.transform(X_test)
    print("Data successfully split into training and testing sets.")
    models = {
        "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(class_weight='balanced', n_estimators=100, random_state=42),
        "SVM": SVC(kernel='linear', class_weight='balanced', random_state=42)
    }
    trained_models = {}
    for name, model in models.items():
        model.fit(X_train_scaled if name == "SVM" else X_train_resampled, y_train_resampled)
        trained_models[name] = model
        print(f"{name} has been successfully trained.")
    performance_results = []
    for name, model in trained_models.items():
        predictions = model.predict(X_test_scaled if name == "SVM" else X_test)
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, average='weighted', zero_division=1)
        recall = recall_score(y_test, predictions, average='weighted', zero_division=1)
        f1 = f1_score(y_test, predictions, average='weighted', zero_division=1)
        print(f"\n{name} Performance Metrics:")
        print(f"Accuracy: {accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1 Score: {f1:.2f}")
        print(f"\n{name} Classification Report:\n")
        print(classification_report(y_test, predictions, zero_division=1))
        performance_results.append({
            "Model": name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1
        })

    comparison_df = pd.DataFrame(performance_results)
    print("\nModel Comparison:")
    print(comparison_df)

    best_model = comparison_df.sort_values(by="F1 Score", ascending=False).iloc[0]
    print(f"\nBest Model Based on F1 Score:\n{best_model}")
