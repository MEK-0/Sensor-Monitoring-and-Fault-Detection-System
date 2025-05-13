import random
import pandas as pd

def generate_data(n=1000):
    data = []

    for _ in range(n):
        # %5 ihtimalle sensör mesafesi 6-40 cm arası olacak
        if random.random() < 0.05:  # %5 ihtimalle 6-40 cm arası mesafe
            sensor_distance = random.uniform(6, 40)
        else:
            # Geri kalan %95'lik kısım 5 ile 6 cm arasında olacak
            sensor_distance = random.uniform(5, 6)

        # Basınç (249.57 kPa ile 400 kPa arasında, %3 ihtimalle 249.57'den düşük olacak)
        pressure = random.uniform(249.57, 400)
        if random.random() < 0.03:  # %3 ihtimalle basınç 249.57'den düşük olacak
            pressure = random.uniform(100, 249.56)

        data.append([sensor_distance, pressure])

    # Dataframe'e çevir
    df = pd.DataFrame(data, columns=["sensor_distance", "pressure"])
    return df


# Veriyi oluştur ve kaydet
if __name__ == "__main__":
    df = generate_data()  # Veriyi oluştur
    df.to_csv("sensor_data.csv", index=False)  # Veriyi CSV dosyasına kaydet
    print("Veri başarıyla oluşturuldu ve kaydedildi.")
