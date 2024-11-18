from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE  # SMOTE eklendi
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

def fetch_data():
    client = MongoClient("mongodb://localhost:27017")
    db = client["thesis_project"]
    collection = db["sample_data"]
    data = pd.DataFrame(list(collection.find()))
    data.drop(columns=['_id'], inplace=True)
    return data

if __name__ == "__main__":
    data = fetch_data()

    # Tarih sütunlarını kontrol edin ve işleyin
    datetime_columns = data.select_dtypes(include=['datetime64']).columns
    for col in datetime_columns:
        data[col] = (data[col] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    # Gereksiz sütunları kaldır
    data = data.drop(columns=['name', 'email', 'location'], errors='ignore')

    # Eksik verileri doldur
    data['category'] = data['category'].fillna('unknown')

    # Hedef değişkeni kodlama
    target_column = "category"
    label_encoder = LabelEncoder()
    data[target_column] = label_encoder.fit_transform(data[target_column])

    # Giriş (X) ve hedef (y) değişkenlerini ayır
    X = data.drop(columns=[target_column])
    y = data[target_column]

    # Veriyi eğitim ve test setlerine ayır
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # SMOTE ile dengesiz sınıfları dengelemek
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # Verileri ölçeklendirme
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_resampled)
    X_test_scaled = scaler.transform(X_test)

    print("Data successfully split into training and testing sets.")

    # Modelleri başlat
    models = {
        "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(class_weight='balanced', n_estimators=100, random_state=42),
        "SVM": SVC(kernel='linear', class_weight='balanced', random_state=42)
    }

    # Modelleri eğit
    trained_models = {}
    for name, model in models.items():
        model.fit(X_train_scaled if name == "SVM" else X_train_resampled, y_train_resampled)
        trained_models[name] = model
        print(f"{name} has been successfully trained.")

    # Test verisi üzerinde tahmin yap ve doğruluk hesapla
    for name, model in trained_models.items():
        accuracy = model.score(X_test_scaled if name == "SVM" else X_test, y_test)
        print(f"{name} accuracy: {accuracy:.2f}")

    # Sınıflandırma raporu oluştur
    for name, model in trained_models.items():
        predictions = model.predict(X_test_scaled if name == "SVM" else X_test)
        print(f"{name} Classification Report:\n")
        print(classification_report(y_test, predictions, zero_division=1))  # zero_division ayarı eklendi

    # Confusion Matrix çiz
    for name, model in trained_models.items():
        predictions = model.predict(X_test_scaled if name == "SVM" else X_test)
        disp = ConfusionMatrixDisplay.from_predictions(y_test, predictions)
        disp.ax_.set_title(f"{name} Confusion Matrix")
        plt.show()
