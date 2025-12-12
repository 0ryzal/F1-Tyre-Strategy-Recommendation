"""
F1 Tyre Strategy - Feature Engineering Script
Process collected data and engineer features for ML model
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder

print("="*60)
print("F1 TYRE STRATEGY - FEATURE ENGINEERING")
print("="*60)

# Check if raw data exists
if not os.path.exists('data/f1_tyre_data.csv'):
    print("❌ Error: data/f1_tyre_data.csv not found!")
    print("   Please run data collection script first.")
    exit(1)

# Load the collected data
print("\n📊 Loading raw data...")
df = pd.read_csv('data/f1_tyre_data.csv')
print(f"Loaded {len(df):,} rows")

# Create track characteristics database
print("\n🏁 Creating track characteristics...")
track_chars = {
    'Bahrain': {'type': 'desert', 'severity': 'high', 'corners': 15, 'length': 5.412},
    'Saudi Arabia': {'type': 'street', 'severity': 'high', 'corners': 27, 'length': 6.174},
    'Australia': {'type': 'street', 'severity': 'medium', 'corners': 14, 'length': 5.278},
    'Azerbaijan': {'type': 'street', 'severity': 'medium', 'corners': 20, 'length': 6.003},
    'Miami': {'type': 'street', 'severity': 'high', 'corners': 19, 'length': 5.412},
    'Monaco': {'type': 'street', 'severity': 'low', 'corners': 19, 'length': 3.337},
    'Spain': {'type': 'permanent', 'severity': 'high', 'corners': 16, 'length': 4.675},
    'Canada': {'type': 'street', 'severity': 'medium', 'corners': 14, 'length': 4.361},
    'Austria': {'type': 'permanent', 'severity': 'medium', 'corners': 10, 'length': 4.318},
    'Great Britain': {'type': 'permanent', 'severity': 'high', 'corners': 18, 'length': 5.891},
    'Hungary': {'type': 'permanent', 'severity': 'high', 'corners': 14, 'length': 4.381},
    'Belgium': {'type': 'permanent', 'severity': 'medium', 'corners': 19, 'length': 7.004},
    'Netherlands': {'type': 'permanent', 'severity': 'high', 'corners': 14, 'length': 4.259},
    'Italy': {'type': 'permanent', 'severity': 'low', 'corners': 11, 'length': 5.793},
    'Singapore': {'type': 'street', 'severity': 'high', 'corners': 23, 'length': 4.940},
    'Japan': {'type': 'permanent', 'severity': 'medium', 'corners': 18, 'length': 5.807},
    'Qatar': {'type': 'permanent', 'severity': 'high', 'corners': 16, 'length': 5.380},
    'United States': {'type': 'permanent', 'severity': 'high', 'corners': 20, 'length': 5.513},
    'Mexico': {'type': 'permanent', 'severity': 'medium', 'corners': 17, 'length': 4.304},
    'Brazil': {'type': 'permanent', 'severity': 'high', 'corners': 15, 'length': 4.309},
    'Las Vegas': {'type': 'street', 'severity': 'low', 'corners': 17, 'length': 6.120},
    'Abu Dhabi': {'type': 'permanent', 'severity': 'high', 'corners': 16, 'length': 5.281},
    'Emilia Romagna': {'type': 'permanent', 'severity': 'medium', 'corners': 19, 'length': 4.909},
    'Portugal': {'type': 'permanent', 'severity': 'medium', 'corners': 15, 'length': 4.653},
    'Turkey': {'type': 'permanent', 'severity': 'high', 'corners': 14, 'length': 5.338},
}

track_df = pd.DataFrame.from_dict(track_chars, orient='index').reset_index()
track_df.columns = ['Country', 'TrackType', 'TyreSeverity', 'TotalCorners', 'TrackLength']
track_df.to_csv('data/track_characteristics.csv', index=False)
print("✓ Track characteristics saved")

# Merge track data
print("\n🔗 Merging track characteristics...")
df = df.merge(track_df, on='Country', how='left')
df['TrackType'] = df['TrackType'].fillna('permanent')
df['TyreSeverity'] = df['TyreSeverity'].fillna('medium')
df['TotalCorners'] = df['TotalCorners'].fillna(df['TotalCorners'].median())
df['TrackLength'] = df['TrackLength'].fillna(df['TrackLength'].median())

# Calculate driver statistics
print("\n👤 Engineering driver performance features...")
driver_stats = df.groupby(['Driver', 'Compound']).agg({
    'LapTime': ['mean', 'std', 'count'],
    'TyreLife': 'mean'
}).reset_index()

driver_stats.columns = ['Driver', 'Compound', 'AvgLapTime', 'StdLapTime', 'LapCount', 'AvgTyreLife']
driver_stats['TyreManagementScore'] = 1 / (1 + driver_stats['StdLapTime'])

df = df.merge(driver_stats[['Driver', 'Compound', 'TyreManagementScore']], 
              on=['Driver', 'Compound'], how='left')

# Create time-based features
print("\n⏱️ Creating time-based features...")
race_lap_counts = df.groupby(['Year', 'Round', 'Driver'])['LapNumber'].max().reset_index()
race_lap_counts.columns = ['Year', 'Round', 'Driver', 'TotalLaps']

df = df.merge(race_lap_counts, on=['Year', 'Round', 'Driver'], how='left')
df['RaceProgress'] = df['LapNumber'] / df['TotalLaps']

df['StintPhase'] = pd.cut(df['TyreLife'], bins=[0, 5, 15, 100], 
                          labels=['early', 'middle', 'late'])

# Calculate tyre degradation
print("\n🔧 Calculating tyre performance metrics...")
df = df.sort_values(['Year', 'Round', 'Driver', 'Stint', 'LapNumber']).reset_index(drop=True)

# Simple degradation calculation
df['TyreDegradation'] = 0.0
for name, group in df.groupby(['Year', 'Round', 'Driver', 'Stint']):
    if len(group) >= 2:
        first_lap_time = group.iloc[0]['LapTime']
        indices = group.index
        for idx in indices:
            tyre_life = df.loc[idx, 'TyreLife']
            lap_time = df.loc[idx, 'LapTime']
            if tyre_life > 0:
                df.loc[idx, 'TyreDegradation'] = (lap_time - first_lap_time) / tyre_life

# Temperature compound score
df['TempCompoundScore'] = 0
df.loc[df['Compound'] == 'SOFT', 'TempCompoundScore'] = 30 - df.loc[df['Compound'] == 'SOFT', 'TrackTemp']
df.loc[df['Compound'] == 'HARD', 'TempCompoundScore'] = df.loc[df['Compound'] == 'HARD', 'TrackTemp'] - 30
df.loc[df['Compound'] == 'MEDIUM', 'TempCompoundScore'] = 0

# Encode categorical variables
print("\n🔢 Encoding categorical variables...")
le_track_type = LabelEncoder()
le_severity = LabelEncoder()
le_stint_phase = LabelEncoder()

df['TrackType_Encoded'] = le_track_type.fit_transform(df['TrackType'])
df['TyreSeverity_Encoded'] = le_severity.fit_transform(df['TyreSeverity'])
df['StintPhase_Encoded'] = le_stint_phase.fit_transform(df['StintPhase'].astype(str))
df['Rainfall_Binary'] = df['Rainfall'].astype(int)

# Select features for modeling
feature_columns = [
    'AirTemp', 'TrackTemp', 'Humidity', 'Rainfall_Binary',
    'TrackType_Encoded', 'TyreSeverity_Encoded', 'TotalCorners', 'TrackLength',
    'LapNumber', 'RaceProgress', 'Stint', 'TyreLife', 'StintPhase_Encoded',
    'TyreManagementScore', 'TyreDegradation', 'TempCompoundScore',
    'Compound'
]

df_features = df[feature_columns].copy()
df_features = df_features.dropna()

print(f"\n✅ Feature engineering complete!")
print(f"Final dataset shape: {df_features.shape}")
print(f"\nTarget distribution:")
print(df_features['Compound'].value_counts())

# Save processed features
df_features.to_csv('data/f1_tyre_features.csv', index=False)
print("\n💾 Features saved to data/f1_tyre_features.csv")

# Save feature names
os.makedirs('model', exist_ok=True)
feature_names = [col for col in feature_columns if col != 'Compound']
joblib.dump(feature_names, 'model/feature_names.pkl')
print("✓ Feature names saved")

print("\n" + "="*60)
print("FEATURE ENGINEERING SUMMARY")
print("="*60)
print(f"Total Features: {len(feature_names)}")
print(f"Total Samples: {len(df_features):,}")
print(f"\nReady for model training!")
