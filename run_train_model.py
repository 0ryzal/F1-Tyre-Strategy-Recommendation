"""
F1 Tyre Strategy - Model Training Script
Train ML model to recommend optimal tyre compounds
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("F1 TYRE STRATEGY - MODEL TRAINING")
print("="*60)

# Check if features exist
if not os.path.exists('data/f1_tyre_features.csv'):
    print("❌ Error: data/f1_tyre_features.csv not found!")
    print("   Please run feature engineering script first.")
    exit(1)

# Load features
print("\n📊 Loading processed features...")
df = pd.read_csv('data/f1_tyre_features.csv')
print(f"Loaded {len(df):,} samples")
print(f"Features: {df.shape[1] - 1}")

# Separate features and target
X = df.drop('Compound', axis=1)
y = df['Compound']

# Encode target variable
le_compound = LabelEncoder()
y_encoded = le_compound.fit_transform(y)

print(f"\nCompound encoding:")
for i, compound in enumerate(le_compound.classes_):
    print(f"  {compound}: {i}")

# Save label encoder
joblib.dump(le_compound, 'model/label_encoder.pkl')
print("\n✓ Label encoder saved")

# Train-test split
print("\n🔀 Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"Training set: {X_train.shape[0]:,} samples")
print(f"Test set: {X_test.shape[0]:,} samples")

# Scale features
print("\n📏 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, 'model/scaler.pkl')
print("✓ Feature scaler saved")

# Train multiple models
print("\n" + "="*60)
print("TRAINING MODELS")
print("="*60)

models = {
    'Random Forest': RandomForestClassifier(
        n_estimators=200, 
        max_depth=20, 
        min_samples_split=10,
        random_state=42,
        n_jobs=-1
    ),
    'Gradient Boosting': GradientBoostingClassifier(
        n_estimators=200,
        max_depth=10,
        learning_rate=0.1,
        random_state=42
    ),
    'XGBoost': XGBClassifier(
        n_estimators=200,
        max_depth=10,
        learning_rate=0.1,
        random_state=42,
        eval_metric='mlogloss'
    )
}

results = {}

for name, model in models.items():
    print(f"\n{'='*50}")
    print(f"Training {name}...")
    print(f"{'='*50}")
    
    # Train
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation
    print("Running cross-validation...")
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    
    results[name] = {
        'model': model,
        'accuracy': accuracy,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'predictions': y_pred
    }
    
    print(f"\nTest Accuracy: {accuracy:.4f}")
    print(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le_compound.classes_, zero_division=0))

# Select best model
print("\n" + "="*60)
print("MODEL COMPARISON")
print("="*60)

comparison_df = pd.DataFrame({
    'Model': list(results.keys()),
    'Test Accuracy': [r['accuracy'] for r in results.values()],
    'CV Mean': [r['cv_mean'] for r in results.values()],
    'CV Std': [r['cv_std'] for r in results.values()]
})

print(comparison_df.to_string(index=False))

# Select best model (highest test accuracy)
best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_model_name]['model']

print(f"\n🏆 Best Model: {best_model_name}")
print(f"   Accuracy: {results[best_model_name]['accuracy']:.4f}")

# Save best model
joblib.dump(best_model, 'model/tyre_recommender.pkl')
joblib.dump(X.columns.tolist(), 'model/feature_columns.pkl')

print("\n💾 Model saved to model/tyre_recommender.pkl")
print("✓ Feature columns saved")

# Test with sample predictions
print("\n" + "="*60)
print("SAMPLE PREDICTIONS")
print("="*60)

sample_scenarios = [
    {
        'name': 'Hot Weather, Early Race',
        'features': {
            'AirTemp': 35, 'TrackTemp': 45, 'Humidity': 40, 'Rainfall_Binary': 0,
            'TrackType_Encoded': 0, 'TyreSeverity_Encoded': 2, 'TotalCorners': 16, 'TrackLength': 5.0,
            'LapNumber': 5, 'RaceProgress': 0.1, 'Stint': 1, 'TyreLife': 5, 'StintPhase_Encoded': 0,
            'TyreManagementScore': 0.8, 'TyreDegradation': 0.02, 'TempCompoundScore': 5
        }
    },
    {
        'name': 'Cool Weather, Mid Race',
        'features': {
            'AirTemp': 18, 'TrackTemp': 25, 'Humidity': 60, 'Rainfall_Binary': 0,
            'TrackType_Encoded': 0, 'TyreSeverity_Encoded': 1, 'TotalCorners': 18, 'TrackLength': 5.5,
            'LapNumber': 30, 'RaceProgress': 0.5, 'Stint': 2, 'TyreLife': 15, 'StintPhase_Encoded': 1,
            'TyreManagementScore': 0.85, 'TyreDegradation': 0.05, 'TempCompoundScore': -5
        }
    }
]

for scenario in sample_scenarios:
    features = pd.DataFrame([scenario['features']])[X.columns]
    features_scaled = scaler.transform(features)
    
    prediction = best_model.predict(features_scaled)
    probabilities = best_model.predict_proba(features_scaled)[0]
    
    predicted_compound = le_compound.inverse_transform(prediction)[0]
    
    print(f"\n{scenario['name']}:")
    print(f"  Recommended: {predicted_compound}")
    print(f"  Confidence:")
    for i, compound in enumerate(le_compound.classes_):
        print(f"    {compound}: {probabilities[i]:.2%}")

print("\n" + "="*60)
print("MODEL TRAINING COMPLETE")
print("="*60)
print(f"\nBest Model: {best_model_name}")
print(f"Test Accuracy: {results[best_model_name]['accuracy']:.4f}")
print(f"CV Accuracy: {results[best_model_name]['cv_mean']:.4f} (+/- {results[best_model_name]['cv_std']:.4f})")
print(f"\nSaved Files:")
print("  - model/tyre_recommender.pkl")
print("  - model/scaler.pkl")
print("  - model/label_encoder.pkl")
print("  - model/feature_columns.pkl")
print("\n✅ Model is ready for deployment!")
