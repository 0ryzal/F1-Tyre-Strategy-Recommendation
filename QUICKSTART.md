# 🏎️ F1 Tyre Strategy Recommender - Quick Start

## ⚠️ Catatan Penting

Proyek ini memerlukan Python 3.11 atau 3.12 untuk instalasi yang lancar di Windows. Python 3.13 mungkin mengalami masalah saat membangun NumPy dari source.

## 🚀 Cara Tercepat - Menggunakan Conda (DIREKOMENDASIKAN)

### 1. Install Miniconda
Download dari: https://docs.conda.io/en/latest/miniconda.html

### 2. Buat Environment & Install Dependencies
```powershell
# Buat environment baru
conda create -n f1tyre python=3.11 -y

# Aktifkan environment
conda activate f1tyre

# Install semua dependencies via conda-forge (CARA TERMUDAH!)
conda install -c conda-forge fastf1 numpy pandas matplotlib seaborn xgboost scikit-learn streamlit joblib plotly jupyter -y
```

### 3. Jalankan Pipeline Lengkap

#### A. Kumpulkan Data (15-30 menit)
```powershell
jupyter notebook collect_data.ipynb
```
Jalankan semua cell dari atas ke bawah. Ini akan mengunduh data F1 dari 2021-2024.

#### B. Build Features (2-5 menit)
```powershell
jupyter notebook build_features.ipynb
```
Jalankan semua cell untuk membuat engineered features.

#### C. Train Model (5-10 menit)
```powershell
jupyter notebook train_model.ipynb
```
Jalankan semua cell untuk melatih model AI.

#### D. Jalankan Aplikasi
```powershell
streamlit run app.py
```

## 📋 Alternatif - Menggunakan Python Virtual Environment

**Hanya jika Anda memiliki Python 3.11 atau 3.12 terinstall!**

```powershell
# Buat venv
python -m venv venv

# Aktifkan venv
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Jika NumPy gagal, coba set temp directory ke D:
$env:TEMP='D:\temp_pip'
$env:TMP='D:\temp_pip'
pip install -r requirements.txt
```

## 🎯 Jika Tidak Ingin Install Lokal

### Opsi A: Google Colab
Upload ketiga notebook ke Google Colab dan jalankan di sana (gratis, tidak perlu install).

### Opsi B: Streamlit Cloud
Deploy langsung ke Streamlit Cloud setelah training model:
1. Push project ke GitHub
2. Buat akun di https://streamlit.io/cloud
3. Connect repository dan deploy `app.py`

## 📂 Struktur File yang Dihasilkan

Setelah menjalankan semua notebook, struktur Anda akan seperti ini:

```
F1TyreStrategy/
├── app.py                          ✅ Aplikasi Streamlit
├── collect_data.ipynb              ✅ Notebook 1
├── build_features.ipynb            ✅ Notebook 2
├── train_model.ipynb               ✅ Notebook 3
├── requirements.txt                ✅ Dependencies
├── data/                           
│   ├── f1_tyre_data.csv           📊 Data mentah (setelah notebook 1)
│   ├── f1_tyre_features.csv       📊 Features (setelah notebook 2)
│   └── track_characteristics.csv   📊 Info track (setelah notebook 2)
└── model/                          
    ├── tyre_recommender.pkl       🤖 Model trained (setelah notebook 3)
    ├── scaler.pkl                 🤖 Scaler (setelah notebook 3)
    ├── label_encoder.pkl          🤖 Encoder (setelah notebook 3)
    └── feature_columns.pkl        🤖 Feature names (setelah notebook 3)
```

## 🔍 Troubleshooting Cepat

### Problem: NumPy gagal install
**Solusi**: Gunakan Conda (paling mudah) atau Python 3.11/3.12

### Problem: FastF1 error saat download
**Solusi**: 
- Pastikan koneksi internet stabil
- Delete folder `cache/` jika ada
- Coba lagi

### Problem: Jupyter tidak ada
**Solusi**:
```powershell
conda install jupyter -y
# atau
pip install jupyter
```

### Problem: Model files not found
**Solusi**: Anda harus menjalankan ketiga notebook secara berurutan dulu sebelum bisa menjalankan `app.py`

## ✅ Checklist Instalasi

- [ ] Install Conda atau Python 3.11/3.12
- [ ] Buat environment
- [ ] Install dependencies
- [ ] Jalankan `collect_data.ipynb` → menghasilkan `data/f1_tyre_data.csv`
- [ ] Jalankan `build_features.ipynb` → menghasilkan `data/f1_tyre_features.csv`
- [ ] Jalankan `train_model.ipynb` → menghasilkan `model/tyre_recommender.pkl`
- [ ] Jalankan `streamlit run app.py`

## 🎮 Cara Menggunakan Aplikasi

1. **Pilih Circuit**: Pilih track F1 dari dropdown
2. **Set Weather**: Atur suhu udara, suhu track, humidity
3. **Race Context**: Lap saat ini, stint, usia ban
4. **Driver Profile**: Pilih gaya berkendara (Conservative/Balanced/Aggressive)
5. **Klik "Get Tyre Recommendation"**: Dapatkan rekomendasi AI!

## 📊 Fitur Aplikasi

- ✅ Rekomendasi compound ban (SOFT/MEDIUM/HARD/INTERMEDIATE/WET)
- ✅ Confidence score untuk setiap compound
- ✅ Analisis kontekstual (kenapa compound ini direkomendasikan)
- ✅ Strategi pit stop (kapan pit, berapa lama stint)
- ✅ Alternatif compound dengan probabilitasnya

## 🏁 Hasil yang Diharapkan

- **Akurasi Model**: 75-85% pada test data
- **Data Training**: 100,000+ lap dari 4 musim F1 (2021-2024)
- **Compounds Supported**: 5 jenis (SOFT, MEDIUM, HARD, INTERMEDIATE, WET)
- **Circuits Supported**: 20+ circuit F1

## 📚 Dokumentasi Lengkap

- `README.md` - Overview proyek
- `SETUP_GUIDE.md` - Panduan lengkap setup
- `MODEL_EXPLANATION.md` - Penjelasan model ML detail
- Notebook comments - Penjelasan di setiap cell

## 🆘 Butuh Bantuan?

1. Baca `SETUP_GUIDE.md` untuk troubleshooting detail
2. Check output error di terminal/notebook
3. Pastikan semua file dependencies ada
4. Cek dokumentasi FastF1: https://docs.fastf1.dev/

---

**Selamat mencoba! Semoga berhasil! 🏎️💨**
