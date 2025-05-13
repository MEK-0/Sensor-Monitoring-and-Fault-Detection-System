import time
import subprocess


def main():
    # Veriyi oluştur
    print("Veri oluşturuluyor...")
    subprocess.run(["python", "generate_sensor_data.py"])
    time.sleep(1)

    # Modeli eğit
    print("Model eğitiliyor...")
    subprocess.run(["python", "model.py"])
    time.sleep(1)

    # GUI'yi başlat
    print("GUI başlatılıyor...")
    subprocess.run(["python", "gui.py"])


if __name__ == "__main__":
    main()
