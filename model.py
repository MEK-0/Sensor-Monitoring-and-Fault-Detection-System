from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd


def train_model():
    # Veriyi yükle
    df = pd.read_csv("sensor_data.csv")

    # Basınç ve mesafeye dayalı özellikler
    X = df[['sensor_distance', 'pressure']]

    # Etiketler (bu örnekte 'label' sabit olacak, ancak bunu gerçek veriye göre değiştirebiliriz)
    y = (df['pressure'] >= 249.57).astype(int)  # Basınç 249.57'nin üzerinde ise 1, değilse 0

    # Eğitim ve test verilerine ayır
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modeli oluştur ve eğit
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Modeli test et
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model doğruluğu: {accuracy * 100:.2f}%")

    # Modeli kaydet
    import joblib
    joblib.dump(model, "sensor_model.pkl")

    return model


# Modeli eğit
if __name__ == "__main__":
    train_model()
