# 🏎️ F1 Tyre Strategy Recommendation System

AI-powered system that recommends optimal tyre compounds for Formula 1 races based on multiple factors including weather conditions, track characteristics, driver style, and historical performance data.

## 📦 Features
- **Smart Tyre Recommendations**: Predicts optimal tyre compound (Soft, Medium, Hard) based on race conditions
- **Multi-Factor Analysis**: Considers weather, temperature, track characteristics, driver style, and more
- **Historical Data**: Trained on real F1 data from FastF1 API
- **Interactive UI**: Easy-to-use Streamlit interface
- **Pit Stop Strategy**: Suggests optimal pit stop windows and tyre change timing

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
streamlit run app.py
```

## 📊 Project Structure
```
F1TyreStrategy/
├── app.py                          # Streamlit application
├── collect_data.ipynb              # Data collection from FastF1
├── build_features.ipynb            # Feature engineering
├── train_model.ipynb               # Model training
├── requirements.txt
├── data/
│   ├── f1_tyre_data.csv           # Raw collected data
│   ├── f1_tyre_features.csv       # Processed features
│   └── track_characteristics.csv   # Track-specific data
└── model/
    ├── tyre_recommender.pkl       # Trained model
    ├── scaler.pkl                 # Feature scaler
    └── feature_columns.pkl        # Feature order

```

## 🧠 Model Features
- **Weather**: Air temperature, track temperature, humidity, rainfall
- **Track**: Circuit type, length, corners, average speed
- **Driver**: Driving style (aggressive/conservative), experience, tyre management rating
- **Race Context**: Stint length, lap number, fuel load, position in race
- **Historical**: Past tyre performance on the circuit

## 🎯 Use Cases
- Race engineers planning pit strategies
- Fantasy F1 players optimizing their picks
- F1 enthusiasts analyzing race strategies
- Data scientists exploring F1 analytics

---

## 🌐 Live App
You can try the live app here:  
**[https://f1-tyre-strategy-recommendation.streamlit.app/]**

---

## 📝 Author
Built with FastF1, Scikit-Learn, XGBoost, and F1 passion 🏁
