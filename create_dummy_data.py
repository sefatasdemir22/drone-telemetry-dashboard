import pandas as pd
import numpy as np

# Senin için özel: Drone Uçuş Verisi Simülasyonu
data = {
    'Ucus_Suresi_dk': np.arange(1, 101),
    'Batarya_Seviyesi': np.linspace(100, 10, 100) + np.random.normal(0, 2, 100), # %100'den %10'a düşüş
    'Yukseklik_m': np.random.normal(50, 10, 100), # Ort 50m yükseklik
    'Hiz_ms': np.random.normal(15, 5, 100),       # Ort 15 m/s hız
    'Sinyal_Gucu_dBm': -1 * np.abs(np.random.normal(40, 10, 100)), # Sinyal gücü
    'Motor_Sicakligi_C': np.linspace(30, 75, 100) + np.random.normal(0, 3, 100) # Isınan motorlar
}

df = pd.DataFrame(data)

# CSV olarak kaydet
df.to_csv('drone_logs.csv', index=False)
print("✅ drone_logs.csv başarıyla oluşturuldu!")