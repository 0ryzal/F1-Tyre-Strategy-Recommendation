# How the F1 Tyre Strategy Model Works

## Overview
This document explains the machine learning approach used to recommend optimal tyre compounds for Formula 1 races.

## Problem Statement
Given current race conditions (weather, track, lap number, driver style), predict which tyre compound (SOFT, MEDIUM, HARD, INTERMEDIATE, WET) will perform best for the next stint.

## Data Collection

### Source
- **FastF1 API**: Official F1 timing and telemetry data
- **Seasons**: 2021-2024 (4 seasons)
- **Granularity**: Individual lap level data

### Raw Data Points
For each lap, we collect:
- Driver identifier
- Lap number and stint number
- Tyre compound used
- Tyre life (laps on current tyres)
- Lap time
- Weather data (air temp, track temp, humidity, rainfall)
- Track information (circuit name, country, location)

### Data Volume
- **~100,000+ laps** analyzed across all seasons
- **~20 circuits** per season
- **20 drivers** per race
- **5 tyre compounds**: SOFT, MEDIUM, HARD, INTERMEDIATE, WET

## Feature Engineering

### 1. Weather Features (4 features)
- **AirTemp**: Ambient air temperature in °C
- **TrackTemp**: Track surface temperature in °C
- **Humidity**: Relative humidity percentage
- **Rainfall_Binary**: Boolean indicator for rain (0=dry, 1=wet)

**Rationale**: Temperature affects tyre working range. Softer compounds work better in cooler temps, harder in heat.

### 2. Track Features (4 features)
- **TrackType_Encoded**: Circuit type (street/permanent)
- **TyreSeverity_Encoded**: Track abrasiveness (low/medium/high)
- **TotalCorners**: Number of corners in the circuit
- **TrackLength**: Circuit length in kilometers

**Rationale**: Track characteristics affect tyre wear rate and compound suitability.

### 3. Race Context Features (5 features)
- **LapNumber**: Current lap in the race
- **RaceProgress**: Percentage of race completed (0-1)
- **Stint**: Which stint number (1st, 2nd, 3rd, etc.)
- **TyreLife**: Laps completed on current tyres
- **StintPhase_Encoded**: Phase of stint (early/middle/late)

**Rationale**: Strategy varies by race phase - aggressive early, conservative late.

### 4. Performance Features (3 features)
- **TyreManagementScore**: Driver's ability to preserve tyres (0-1)
  - Calculated from lap time consistency within stints
  - Higher score = better tyre management
  
- **TyreDegradation**: Rate of lap time increase per lap
  - Measured as: (current_lap_time - first_lap_time) / tyre_life
  
- **TempCompoundScore**: Temperature-compound interaction score
  - SOFT: performs better in cooler conditions (score = 30 - track_temp)
  - HARD: performs better in hot conditions (score = track_temp - 30)
  - MEDIUM: neutral (score = 0)

**Rationale**: Driver skill and current tyre condition heavily influence optimal compound choice.

## Model Architecture

### Approach
**Multi-class Classification Problem**
- Input: 16 engineered features
- Output: Probability distribution over 5 compound classes
- Recommendation: Compound with highest probability

### Models Evaluated

1. **Random Forest Classifier**
   - Ensemble of 200 decision trees
   - Max depth: 20
   - Handles non-linear relationships well
   - Good baseline performance

2. **Gradient Boosting Classifier**
   - Sequential tree building
   - 200 estimators
   - Learning rate: 0.1
   - Better at capturing complex patterns

3. **XGBoost Classifier**
   - Advanced gradient boosting
   - Regularization to prevent overfitting
   - Generally best performance
   - Handles missing data well

### Model Selection
- Train all three models
- Compare using 5-fold cross-validation
- Select model with highest test accuracy
- Typical best performer: **XGBoost** (75-85% accuracy)

## Training Process

### 1. Data Preparation
```
Total Dataset → Split (80/20) → Train Set | Test Set
                                    ↓
                               Stratified Split
                           (maintain class balance)
```

### 2. Feature Scaling
- Apply **StandardScaler** to normalize features
- Formula: z = (x - mean) / std_dev
- Prevents features with large ranges from dominating

### 3. Training
- Fit model on training set
- Use class weights to handle imbalanced data
- Soft/Medium compounds more common than Wet/Intermediate

### 4. Validation
- 5-fold cross-validation on training set
- Evaluate on held-out test set
- Metrics: Accuracy, Precision, Recall, F1-Score per class

### 5. Feature Importance Analysis
- Identify most influential features
- Typical top features:
  1. TrackTemp (critical for compound performance)
  2. TyreLife (when to change tyres)
  3. TyreSeverity (track wear characteristics)
  4. RaceProgress (strategic considerations)
  5. Rainfall (wet vs dry tyres)

## Prediction Process

### Input Processing
1. User provides race parameters via Streamlit UI
2. Features extracted and arranged in correct order
3. Features scaled using saved StandardScaler

### Model Inference
1. Scaled features fed to trained model
2. Model outputs probability for each compound
3. Probabilities sum to 1.0 (100%)

### Recommendation Logic
```python
# Example output
Probabilities:
  SOFT: 0.65 (65%)     ← Recommended
  MEDIUM: 0.25 (25%)
  HARD: 0.08 (8%)
  INTERMEDIATE: 0.01 (1%)
  WET: 0.01 (1%)
```

### Confidence Threshold
- High confidence: >50% probability
- Medium confidence: 30-50%
- Low confidence: <30% (show alternatives)

## Model Interpretability

### Context-Aware Reasoning
The app provides explanations based on:

1. **Weather-based**
   - Rain detected → recommend WET/INTERMEDIATE
   - High track temp → recommend HARD
   - Cool track temp → recommend SOFT

2. **Race-phase based**
   - Early race → optimize for speed (SOFT)
   - Mid race → balance (MEDIUM)
   - Late race → durability (HARD)

3. **Track-based**
   - High severity → prioritize durability
   - Low severity → can use softer compounds

4. **Driver-based**
   - Aggressive style → need more durable tyres
   - Conservative style → can use softer compounds longer

## Model Limitations

### Known Constraints
1. **Historical Bias**: Trained on past decisions, may not predict revolutionary strategies
2. **Weather Uncertainty**: Predictions assume conditions remain stable
3. **Driver Variability**: Generic driver profiles, not personalized
4. **Team Strategy**: Doesn't account for competitor strategies
5. **Regulation Changes**: 2021-2024 data may not apply to future rule changes

### Areas for Improvement
- Incorporate real-time telemetry data
- Add pit stop loss modeling
- Consider tyre allocation rules
- Include safety car probabilities
- Model tyre compound age (not just lap count)

## Performance Metrics

### Expected Accuracy
- **Overall**: 75-85%
- **Dry conditions**: 80-85% (more data available)
- **Wet conditions**: 65-75% (less frequent, harder to predict)

### Per-Compound Performance
- **SOFT**: High precision (commonly used correctly)
- **MEDIUM**: Good balance
- **HARD**: Lower recall (used less often)
- **INTERMEDIATE/WET**: Variable (weather-dependent)

## Practical Applications

### Use Cases
1. **Race Engineers**: Quick strategy assessment tool
2. **Fantasy F1**: Predict tyre strategies for game decisions
3. **F1 Education**: Learn how conditions affect tyre choice
4. **Data Analysis**: Explore historical tyre usage patterns

### Real-World Validation
Compare model predictions with actual race outcomes to validate performance.

## Technical Stack

- **Data**: FastF1 API
- **Processing**: Pandas, NumPy
- **ML**: Scikit-learn, XGBoost
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Interface**: Streamlit
- **Storage**: Joblib (model persistence)

## Conclusion

The F1 Tyre Strategy Recommender uses machine learning to distill patterns from 100,000+ historical laps into actionable recommendations. By combining weather, track, race context, and driver characteristics, it provides informed suggestions for optimal tyre compound selection.

The model balances accuracy with interpretability, offering not just predictions but contextual reasoning to help users understand the recommendation logic.

---

**For Technical Details**: See source code in notebooks
**For Usage**: See SETUP_GUIDE.md and README.md
