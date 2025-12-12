# 🏎️ Panduan Mendapatkan Rekomendasi Tyre HARD atau SOFT

## 📊 Mengapa Selalu Dapat MEDIUM?

Model AI dilatih dengan data nyata F1 2023-2024, dan MEDIUM adalah compound yang paling sering digunakan dalam berbagai kondisi karena keserbagunaannya. Untuk mendapatkan rekomendasi **HARD** atau **SOFT**, Anda perlu mengatur parameter tertentu.

---

## 🔥 Cara Mendapatkan Rekomendasi **HARD**

Compound HARD cocok untuk kondisi track yang **sangat panas** dan **high degradation**.

### ✅ Parameter Yang Harus Diatur:

1. **Track Temperature**: **45-55°C** (sangat panas!)
   - Slide track temp ke angka maksimal (55°C)

2. **Air Temperature**: **35-45°C** 
   - Set di atas 35°C

3. **Humidity**: **20-40%** (rendah)
   - Humidity rendah = track lebih panas

4. **Circuit Selection**: Pilih circuit dengan **High Tyre Severity**
   - **Bahrain** (desert, high severity)
   - **Saudi Arabia** (street, high severity)  
   - **Singapore** (street, high severity)
   - **Abu Dhabi** (desert, high severity)

5. **Tyre Life**: **15-30 laps** 
   - Tyre sudah mengalami degradasi tinggi
   - Model akan rekomendasikan compound yang lebih keras

6. **Race Progress**: **> 50%**
   - Lap number: 30-50
   - Total laps: 58
   - Late race dengan stint terakhir memerlukan compound yang awet

7. **Driver Style**: **Aggressive**
   - Aggressive style cenderung pakai compound lebih keras

### 🎯 Contoh Setting untuk HARD:

```
Circuit: Bahrain (high severity)
Air Temp: 40°C
Track Temp: 52°C
Humidity: 25%
Rainfall: ❌ NO
Current Lap: 35
Total Laps: 58
Stint: 2
Tyre Life: 25 laps
Driver Style: Aggressive
```

---

## ❄️ Cara Mendapatkan Rekomendasi **SOFT**

Compound SOFT cocok untuk kondisi track yang **dingin**, **awal race**, atau **fresh tyres**.

### ✅ Parameter Yang Harus Diatur:

1. **Track Temperature**: **20-30°C** (dingin!)
   - Slide track temp ke angka minimum (20-25°C)

2. **Air Temperature**: **15-25°C**
   - Set di bawah 25°C

3. **Humidity**: **60-90%** (tinggi)
   - Humidity tinggi = track lebih dingin

4. **Circuit Selection**: Pilih circuit dengan **Low/Medium Severity**
   - **Monaco** (street, low severity) - sangat lambat
   - **Hungary** (permanent, medium)
   - **Singapore** (street, medium)
   - **Canada** (street, medium)

5. **Tyre Life**: **0-5 laps** (fresh tyres!)
   - Set tyre life ke 0-3 laps
   - Fresh tyres = bisa pakai soft

6. **Race Progress**: **< 30%**
   - Lap number: 1-15
   - Total laps: 58
   - Awal race dengan stint pertama

7. **Driver Style**: **Conservative**
   - Conservative style bisa manage soft compound

8. **Stint**: **1** (stint pertama)
   - Stint phase akan otomatis "Early"

### 🎯 Contoh Setting untuk SOFT:

```
Circuit: Monaco (low severity)
Air Temp: 20°C
Track Temp: 24°C
Humidity: 75%
Rainfall: ❌ NO
Current Lap: 3
Total Laps: 58
Stint: 1
Tyre Life: 2 laps
Driver Style: Conservative
```

---

## 🌧️ Cara Mendapatkan INTERMEDIATE / WET

Ini paling mudah - cukup centang **Rainfall** ✅

### ✅ Parameter:

1. **Rainfall**: ✅ **YES**
2. Track temp dan air temp bisa berapa saja
3. Model otomatis akan rekomendasikan INTERMEDIATE atau WET

---

## 📈 Logika Model AI

Model mempertimbangkan 16 features:

### 🌡️ Weather Features (40%):
- **AirTemp** ⬆️ = HARDER compound
- **TrackTemp** ⬆️⬆️ = HARDER compound (paling berpengaruh!)
- **Humidity** ⬇️ = HARDER compound
- **Rainfall** = INTERMEDIATE/WET

### 🏁 Track Features (30%):
- **High Tyre Severity** = HARDER compound
- **Many Corners** = more degradation = HARDER
- **Long Track** = more degradation = HARDER

### ⏱️ Race Context (20%):
- **Late Race (> 50%)** = HARDER (need durability)
- **Early Race (< 30%)** = SOFTER (can push)
- **High Tyre Life** = time to switch to HARDER

### 👤 Driver Style (10%):
- **Aggressive** = HARDER compound
- **Conservative** = SOFTER compound (can manage)

---

## 🎮 Strategi Cepat

### Untuk **HARD** - Gunakan Preset Ini:
1. **Bahrain** + **55°C track** + **Lap 40/58** + **25 tyre life** = HARD
2. **Saudi Arabia** + **50°C track** + **Aggressive** = HARD
3. **Abu Dhabi** + **52°C track** + **Late race** = HARD

### Untuk **SOFT** - Gunakan Preset Ini:
1. **Monaco** + **22°C track** + **Lap 1** + **0 tyre life** = SOFT
2. **Hungary** + **25°C track** + **Conservative** + **Early race** = SOFT
3. **Singapore** + **28°C track** + **Fresh tyres** + **Stint 1** = SOFT

### Untuk **WET/INTERMEDIATE**:
1. Centang **Rainfall** ✅ pada circuit manapun = WET/INTERMEDIATE

---

## 🔬 Verifikasi Data Training

Dari data training (37,544 laps):

### Distribusi Compound:
- **MEDIUM**: ~40-50% (paling banyak)
- **SOFT**: ~25-30% 
- **HARD**: ~15-20%
- **INTERMEDIATE**: ~5-10%
- **WET**: ~2-5%

### Track Temp Distribution:
- **SOFT**: avg 25-32°C
- **MEDIUM**: avg 28-40°C  
- **HARD**: avg 38-50°C
- **WET/INT**: any temp with rain

---

## 💡 Tips Expert

1. **Kombinasi Extreme = Hasil Extreme**
   - Track temp 55°C + High severity + Late race = HARD
   - Track temp 20°C + Low severity + Early race = SOFT

2. **Gunakan Circuit Characteristics**
   - Street circuits + Hot = HARD
   - Street circuits + Cold = SOFT
   - Permanent + Moderate = MEDIUM

3. **Race Strategy**
   - One-stop strategy: Start SOFT → Finish HARD
   - Two-stop strategy: SOFT → MEDIUM → SOFT
   - Three-stop: SOFT → SOFT → MEDIUM → SOFT

4. **Confidence Score**
   - Jika confidence MEDIUM > 80% = kondisi optimal untuk medium
   - Coba ubah 2-3 parameter sekaligus untuk shift ke HARD/SOFT

---

## 🚨 Troubleshooting

### "Kenapa tetap dapat MEDIUM?"

Kemungkinan penyebab:
1. **Track temp masih moderate (30-40°C)** → Naikkan ke 50°C+ atau turunkan ke 20°C
2. **Tyre life moderate (5-15 laps)** → Set ke 0-3 (SOFT) atau 20+ (HARD)
3. **Race progress di tengah** → Set early (< lap 10) atau late (> lap 40)
4. **Circuit severity medium** → Pilih high severity atau low severity

### "Confidence terlalu rendah?"

Artinya kondisi Anda ambiguous. Coba:
1. Extreme-kan 1 parameter (track temp sangat tinggi/rendah)
2. Align semua parameter ke satu direction (semua ke HARD atau semua ke SOFT)
3. Gunakan preset circuits yang jelas karakternya

---

## 📞 Quick Reference Card

| Goal | Track Temp | Lap Number | Tyre Life | Circuit Severity | Driver |
|------|------------|------------|-----------|------------------|--------|
| **HARD** | 48-55°C | 30-50 | 20-30 | High | Aggressive |
| **MEDIUM** | 30-42°C | 10-40 | 5-15 | Medium | Balanced |
| **SOFT** | 20-28°C | 1-15 | 0-5 | Low | Conservative |
| **WET/INT** | Any | Any | Any | Any | Any + ✅ Rain |

---

Selamat mencoba! Gunakan kombinasi parameter di atas untuk mendapatkan rekomendasi HARD atau SOFT sesuai kebutuhan strategi race Anda! 🏁🏎️
