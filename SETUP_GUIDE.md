# F1 Tyre Strategy Recommender - Setup Guide

## Prerequisites
- Python 3.11 or higher (recommended)
- pip package manager
- Virtual environment (recommended)

## Installation Steps

### 1. Create Virtual Environment (Recommended)

#### Option A: Using venv (Standard Python)
```powershell
# Navigate to project directory
cd D:\Documents\Rizal\Project\F1TyreStrategy

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

#### Option B: Using Conda (Recommended for Windows)
```powershell
# Create conda environment
conda create -n f1tyre python=3.11 -y

# Activate environment
conda activate f1tyre

# Install pip packages
pip install -r requirements.txt
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

**Note:** If you encounter issues with NumPy installation on Windows:
- Use Python 3.11 or 3.12 (better wheel support)
- Or use Conda: `conda install -c conda-forge fastf1 numpy pandas scikit-learn xgboost streamlit`

### 3. Data Collection & Model Training

#### Step 1: Collect F1 Data
Open and run all cells in `collect_data.ipynb`:
```powershell
jupyter notebook collect_data.ipynb
```
This will collect race data from FastF1 API (2021-2024 seasons).
- Output: `data/f1_tyre_data.csv`
- Time: ~15-30 minutes depending on your connection

#### Step 2: Feature Engineering
Open and run all cells in `build_features.ipynb`:
```powershell
jupyter notebook build_features.ipynb
```
This creates engineered features for the model.
- Output: `data/f1_tyre_features.csv`, `data/track_characteristics.csv`
- Time: ~2-5 minutes

#### Step 3: Train Model
Open and run all cells in `train_model.ipynb`:
```powershell
jupyter notebook train_model.ipynb
```
This trains the ML model for tyre recommendations.
- Output: `model/tyre_recommender.pkl`, `model/scaler.pkl`, etc.
- Time: ~5-10 minutes

### 4. Run the Streamlit App
```powershell
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Quick Start (If Model Already Trained)

If the model files already exist in the `model/` directory:
```powershell
streamlit run app.py
```

## Project Structure
```
F1TyreStrategy/
├── app.py                          # Streamlit web application
├── collect_data.ipynb              # Data collection from FastF1
├── build_features.ipynb            # Feature engineering
├── train_model.ipynb               # Model training
├── requirements.txt                # Python dependencies
├── SETUP_GUIDE.md                  # This file
├── README.md                       # Project documentation
├── data/                           # Data files
│   ├── f1_tyre_data.csv           # Raw collected data
│   ├── f1_tyre_features.csv       # Processed features
│   └── track_characteristics.csv   # Track-specific data
└── model/                          # Trained models
    ├── tyre_recommender.pkl       # Main model
    ├── scaler.pkl                 # Feature scaler
    ├── label_encoder.pkl          # Target encoder
    └── feature_columns.pkl        # Feature order

```

## Troubleshooting

### Issue: NumPy build fails on Windows
**Solution:** 
- Use Python 3.11 or 3.12 (not 3.13)
- Or install via Conda: `conda install numpy`

### Issue: FastF1 cache errors
**Solution:**
- Delete the `cache/` folder and re-run data collection
- Ensure stable internet connection

### Issue: Model files not found
**Solution:**
- Run all three notebooks in order: collect_data → build_features → train_model
- Check that files exist in `model/` directory

### Issue: Streamlit won't start
**Solution:**
```powershell
# Reinstall streamlit
pip uninstall streamlit
pip install streamlit

# Run with full path
python -m streamlit run app.py
```

### Issue: Out of disk space during pip install
**Solution:**
```powershell
# Set temp directory to D: drive
$env:TEMP='D:\temp_pip'
$env:TMP='D:\temp_pip'
pip install -r requirements.txt
```

## System Requirements

### Minimum:
- RAM: 4GB
- Storage: 2GB free space
- Internet: For FastF1 data download

### Recommended:
- RAM: 8GB+
- Storage: 5GB+ free space
- Internet: Broadband connection

## Features in the App

1. **Circuit Selection**: Choose from 20+ F1 circuits
2. **Weather Input**: Air temp, track temp, humidity, rainfall
3. **Race Context**: Current lap, stint info, tyre life
4. **Driver Profile**: Driving style affects recommendations
5. **Real-time Recommendations**: AI predicts optimal tyre compound
6. **Confidence Scores**: See probability for each compound
7. **Strategy Suggestions**: Pit window and stint length estimates

## Data Sources

- **FastF1 API**: Official F1 timing and telemetry data
- **Seasons**: 2021, 2022, 2023, 2024
- **Data Points**: 100,000+ laps analyzed
- **Features**: 16 engineered features

## Model Performance

Expected accuracy: **75-85%** on test data
- Best for: Dry weather conditions
- Compounds: SOFT, MEDIUM, HARD, INTERMEDIATE, WET

## Support

For issues or questions:
1. Check this guide first
2. Review notebook outputs for errors
3. Ensure all dependencies installed correctly
4. Check FastF1 documentation: https://docs.fastf1.dev/

## Next Steps

After setup:
1. Explore the Streamlit app
2. Try different race scenarios
3. Experiment with driver profiles
4. Compare predictions with real race data
5. Fine-tune model parameters in `train_model.ipynb`

Happy Racing! 🏎️🏁
