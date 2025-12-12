# 🚀 How to Push to GitHub

## Step 1: Check Git Status
Pertama, pastikan Git sudah terinstall dan cek status repository:

```powershell
cd "d:\Documents\Rizal\Project\F1TyreStrategy"
git status
```

## Step 2: Initialize Git (jika belum)
Jika belum ada Git repository:

```powershell
git init
```

## Step 3: Remove Existing Remote (jika ada)
Jika sudah ada remote lama yang salah:

```powershell
git remote remove origin
```

## Step 4: Add All Files
Tambahkan semua files ke staging:

```powershell
git add .
```

## Step 5: Commit Changes
Commit dengan pesan yang jelas:

```powershell
git commit -m "Initial commit: F1 Tyre Strategy Recommender with ML & Streamlit UI"
```

## Step 6: Create Repository di GitHub
1. Buka https://github.com
2. Login ke akun GitHub Anda (0ryzal)
3. Klik tombol **"+"** di pojok kanan atas → **"New repository"**
4. Isi form:
   - **Repository name**: `F1-Tyre-Strategy-AI`
   - **Description**: `AI-powered F1 tyre compound recommender using XGBoost ML model with professional Streamlit UI`
   - **Visibility**: Public (atau Private jika mau)
   - **JANGAN** centang "Add a README file" (karena kita sudah punya)
   - **JANGAN** pilih .gitignore (karena sudah ada)
5. Klik **"Create repository"**

## Step 7: Connect to GitHub Remote
Ganti `YOUR-NEW-REPO-URL` dengan URL yang diberikan GitHub:

```powershell
git remote add origin https://github.com/0ryzal/F1-Tyre-Strategy-AI.git
```

Atau jika pakai SSH:

```powershell
git remote add origin git@github.com:0ryzal/F1-Tyre-Strategy-AI.git
```

## Step 8: Rename Branch to Main (jika perlu)
GitHub default branch sekarang adalah `main`, bukan `master`:

```powershell
git branch -M main
```

## Step 9: Push to GitHub
Push semua files ke GitHub:

```powershell
git push -u origin main
```

Jika diminta username/password:
- **Username**: 0ryzal
- **Password**: Gunakan **Personal Access Token** (bukan password GitHub biasa)

### Cara Membuat Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Pilih scope: `repo` (full control)
4. Generate token
5. **COPY TOKEN** (tidak bisa dilihat lagi!)
6. Paste sebagai password saat push

## Step 10: Verify
Cek di browser: `https://github.com/0ryzal/F1-Tyre-Strategy-AI`

---

## 📋 Quick Commands (Copy Paste Ini):

```powershell
# Navigasi ke folder project
cd "d:\Documents\Rizal\Project\F1TyreStrategy"

# Initialize Git (jika belum)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: F1 Tyre Strategy AI with XGBoost ML & Streamlit UI"

# Rename branch
git branch -M main

# Add remote (ganti URL dengan repo Anda)
git remote add origin https://github.com/0ryzal/F1-Tyre-Strategy-AI.git

# Push
git push -u origin main
```

---

## 🔧 Troubleshooting

### Error: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/0ryzal/F1-Tyre-Strategy-AI.git
```

### Error: "failed to push some refs"
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: Authentication failed
- Gunakan Personal Access Token, bukan password
- Atau setup SSH keys

### File terlalu besar?
Cek file yang besar:
```powershell
Get-ChildItem -Recurse | Where-Object {$_.Length -gt 100MB} | Select-Object FullName, @{Name="SizeMB";Expression={[math]::Round($_.Length/1MB,2)}}
```

---

## 📦 Files yang Akan Di-push

Files yang akan di-upload (sudah filtered oleh .gitignore):
- ✅ Source code (.py files)
- ✅ Notebooks (.ipynb)
- ✅ Documentation (.md files)
- ✅ Requirements.txt
- ✅ Model files (model/*.pkl)
- ✅ Data files (data/*.csv)
- ❌ Virtual environment (venv/)
- ❌ Cache folder (cache/)
- ❌ Python cache (__pycache__/)
- ❌ Backup files (*_old.py)

---

## 🎯 Recommended Repository Settings

Setelah push, tambahkan di GitHub:

### Topics (untuk SEO):
- `formula1`
- `f1`
- `machine-learning`
- `xgboost`
- `streamlit`
- `tyre-strategy`
- `fastf1`
- `python`
- `ai`
- `racing`

### README Badge Ideas:
```markdown
![Python](https://img.shields.io/badge/Python-3.13-blue)
![ML](https://img.shields.io/badge/ML-XGBoost-orange)
![UI](https://img.shields.io/badge/UI-Streamlit-red)
![Accuracy](https://img.shields.io/badge/Accuracy-99.97%25-brightgreen)
```

---

Selamat! Repository Anda sudah siap di GitHub! 🚀
