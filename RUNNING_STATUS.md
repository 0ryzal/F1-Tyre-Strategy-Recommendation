# 🏎️ F1 Tyre Strategy Recommender - Cara Menjalankan

## Status: Data Collection sedang berjalan...

Data collection dari FastF1 API sedang berlangsung di background. Proses ini memakan waktu sekitar **10-15 menit** untuk mengunduh data dari musim 2023-2024.

## Cara Menjalankan Lengkap

### Opsi 1: Menjalankan Pipeline Lengkap (OTOMATIS)

Jika data collection sudah selesai, jalankan:

```powershell
cd D:\Documents\Rizal\Project\F1TyreStrategy
python run_pipeline.py
```

Script ini akan menjalankan:
1. Data Collection (atau skip jika sudah ada)
2. Feature Engineering
3. Model Training

### Opsi 2: Menjalankan Step-by-Step (MANUAL)

#### Step 1: Data Collection (✅ SEDANG BERJALAN)
```powershell
python run_collect_data.py
```
**Waktu**: ~10-15 menit
**Output**: `data/f1_tyre_data.csv`

#### Step 2: Feature Engineering
Setelah Step 1 selesai:
```powershell
python run_build_features.py
```
**Waktu**: ~30 detik
**Output**: `data/f1_tyre_features.csv`, `data/track_characteristics.csv`

#### Step 3: Model Training
Setelah Step 2 selesai:
```powershell
python run_train_model.py
```
**Waktu**: ~2-3 menit
**Output**: `model/tyre_recommender.pkl`, `model/scaler.pkl`, dll

#### Step 4: Jalankan Aplikasi Streamlit
Setelah semua step selesai:
```powershell
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## Status Saat Ini

✅ Environment setup - SELESAI
✅ Dependencies installed - SELESAI
🔄 Data collection - SEDANG BERJALAN (background)
⏳ Feature engineering - MENUNGGU
⏳ Model training - MENUNGGU
⏳ Streamlit app - MENUNGGU

## Cara Cek Status Data Collection

Buka terminal dan lihat output. Anda akan melihat:
- "Processing: Round X - [Race Name]"
- "✓ Collected XXX laps"

Ketika selesai, akan muncul:
```
DATA COLLECTION SUMMARY
Total Laps Collected: X,XXX
✅ Data collection complete!
```

## Estimasi Waktu Total

- Data Collection: **10-15 menit** ✅ (sedang berjalan)
- Feature Engineering: **30 detik**
- Model Training: **2-3 menit**
- **TOTAL: ~15-20 menit**

## Troubleshooting

### Jika data collection error:
```powershell
# Hapus cache dan coba lagi
rm -r cache
python run_collect_data.py
```

### Jika script tidak ditemukan:
```powershell
# Pastikan Anda di directory yang benar
cd D:\Documents\Rizal\Project\F1TyreStrategy
ls *.py
```

### Jika module tidak ditemukan:
```powershell
# Gunakan venv python
D:/Documents/Rizal/Project/F1TyreStrategy/venv/Scripts/python.exe run_pipeline.py
```

## File Yang Akan Dihasilkan

Setelah pipeline lengkap:

```
F1TyreStrategy/
├── data/
│   ├── f1_tyre_data.csv              ✅ Raw data (~50MB)
│   ├── f1_tyre_features.csv          ⏳ Processed features
│   └── track_characteristics.csv     ⏳ Track info
├── model/
│   ├── tyre_recommender.pkl          ⏳ Trained model
│   ├── scaler.pkl                    ⏳ Feature scaler
│   ├── label_encoder.pkl             ⏳ Target encoder
│   └── feature_columns.pkl           ⏳ Feature names
└── cache/                            ✅ FastF1 cache
```

## Next Steps

1. **Tunggu data collection selesai** (~5-10 menit lagi)
2. **Jalankan feature engineering**: `python run_build_features.py`
3. **Train model**: `python run_train_model.py`
4. **Launch app**: `streamlit run app.py`

Atau jalankan semuanya otomatis:
```powershell
python run_pipeline.py
```

## Tips

- **Jangan close terminal** saat data collection berjalan
- **Check progress** dengan melihat output terminal
- **Pastikan internet stabil** untuk download data dari FastF1
- **First run takes longer** (downloading data), subsequent runs akan lebih cepat karena ada cache

---

**Status Update: 12 Dec 2025, 9:30 AM**
✅ Environment ready
🔄 Collecting F1 data from 2023-2024 seasons...

**Estimated completion: 9:45 AM**
