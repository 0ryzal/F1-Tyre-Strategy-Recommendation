"""
F1 Tyre Strategy - Data Collection Script
Collects F1 data from FastF1 API (2021-2024 seasons)
"""

import fastf1
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import os

warnings.filterwarnings('ignore')

# Create data and cache directories if not exist
os.makedirs('data', exist_ok=True)
os.makedirs('cache', exist_ok=True)

print("="*60)
print("F1 TYRE STRATEGY - DATA COLLECTION")
print("="*60)

# Enable FastF1 cache for faster data loading
fastf1.Cache.enable_cache('cache')
print("✓ FastF1 initialized successfully!")
print()

# Define years and seasons to collect
years = [2023, 2024]  # Starting with recent years for faster processing
all_data = []

for year in years:
    print(f"\n{'='*50}")
    print(f"Collecting data for {year} season...")
    print(f"{'='*50}")
    
    try:
        schedule = fastf1.get_event_schedule(year)
        races = schedule[schedule['EventFormat'] == 'conventional']
        
        for idx, race in races.iterrows():
            round_num = race['RoundNumber']
            event_name = race['EventName']
            
            try:
                print(f"\nProcessing: Round {round_num} - {event_name}")
                
                # Load race session
                session = fastf1.get_session(year, round_num, 'R')
                session.load()
                
                # Get weather data
                weather = session.weather_data
                if len(weather) > 0:
                    avg_air_temp = weather['AirTemp'].mean()
                    avg_track_temp = weather['TrackTemp'].mean()
                    avg_humidity = weather['Humidity'].mean()
                    rainfall = weather['Rainfall'].sum() > 0
                else:
                    avg_air_temp = avg_track_temp = avg_humidity = np.nan
                    rainfall = False
                
                # Get laps data with tyre information
                laps = session.laps
                laps = laps[laps['LapTime'].notna()]
                
                # Process each lap
                for _, lap in laps.iterrows():
                    try:
                        driver = lap['Driver']
                        compound = lap['Compound']
                        tyre_life = lap['TyreLife']
                        lap_time = lap['LapTime'].total_seconds() if pd.notna(lap['LapTime']) else np.nan
                        lap_number = lap['LapNumber']
                        
                        # Skip if no compound info
                        if pd.isna(compound) or compound == '':
                            continue
                        
                        data_point = {
                            'Year': year,
                            'Round': round_num,
                            'EventName': event_name,
                            'Country': race['Country'],
                            'Location': race['Location'],
                            'Driver': driver,
                            'LapNumber': lap_number,
                            'Compound': compound,
                            'TyreLife': tyre_life,
                            'LapTime': lap_time,
                            'AirTemp': avg_air_temp,
                            'TrackTemp': avg_track_temp,
                            'Humidity': avg_humidity,
                            'Rainfall': rainfall,
                            'IsPersonalBest': lap['IsPersonalBest'],
                            'Stint': lap['Stint'],
                            'FreshTyre': lap['FreshTyre']
                        }
                        
                        all_data.append(data_point)
                    
                    except Exception as e:
                        continue
                
                print(f"  ✓ Collected {len(laps)} laps")
                
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                continue
    
    except Exception as e:
        print(f"Error loading {year} schedule: {e}")
        continue

print(f"\n{'='*50}")
print(f"Total data points collected: {len(all_data)}")
print(f"{'='*50}")

# Convert to DataFrame
print("\n📊 Creating DataFrame...")
df = pd.DataFrame(all_data)

print(f"DataFrame Shape: {df.shape}")

# Basic cleaning
print("\n🧹 Cleaning data...")
initial_count = len(df)

# Remove invalid lap times
df = df[df['LapTime'].notna()]
df = df[df['LapTime'] > 0]

# Remove outliers (lap times > 200 seconds usually are errors)
df = df[df['LapTime'] < 200]

# Keep only relevant compounds (SOFT, MEDIUM, HARD, INTERMEDIATE, WET)
valid_compounds = ['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET']
df = df[df['Compound'].isin(valid_compounds)]

print(f"Data after cleaning: {len(df)} rows (removed {initial_count - len(df)} rows)")
print("\nCompound Distribution:")
print(df['Compound'].value_counts())

# Save to CSV
print("\n💾 Saving data...")
df.to_csv('data/f1_tyre_data.csv', index=False)
print("✓ Data saved to data/f1_tyre_data.csv")

# Display summary statistics
print("\n" + "="*60)
print("DATA COLLECTION SUMMARY")
print("="*60)
print(f"Total Laps Collected: {len(df):,}")
print(f"Years Covered: {df['Year'].min()} - {df['Year'].max()}")
print(f"Unique Races: {df['EventName'].nunique()}")
print(f"Unique Drivers: {df['Driver'].nunique()}")
print(f"\nCompounds:")
for compound in df['Compound'].unique():
    count = len(df[df['Compound'] == compound])
    pct = (count / len(df)) * 100
    print(f"  {compound}: {count:,} laps ({pct:.1f}%)")

print("\n✅ Data collection complete!")
