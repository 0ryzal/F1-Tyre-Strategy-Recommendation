"""
F1 Tyre Strategy - Complete Pipeline Runner
Runs the complete workflow from data collection to model training
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*70}")
    print(f"STEP: {description}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error in {description}")
        print(f"Exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Script not found: {script_name}")
        return False

def main():
    print("="*70)
    print(" "*15 + "F1 TYRE STRATEGY RECOMMENDER")
    print(" "*20 + "Complete Pipeline Runner")
    print("="*70)
    
    # Check if we should skip data collection (if data already exists)
    skip_collection = False
    if os.path.exists('data/f1_tyre_data.csv'):
        print("\n⚠️  Data file already exists: data/f1_tyre_data.csv")
        response = input("Skip data collection? (y/n): ").lower().strip()
        if response == 'y':
            skip_collection = True
            print("✓ Skipping data collection")
    
    # Step 1: Data Collection
    if not skip_collection:
        success = run_script('run_collect_data.py', 'Data Collection (10-15 minutes)')
        if not success:
            print("\n❌ Pipeline stopped due to error in data collection")
            return
    
    # Step 2: Feature Engineering
    success = run_script('run_build_features.py', 'Feature Engineering')
    if not success:
        print("\n❌ Pipeline stopped due to error in feature engineering")
        return
    
    # Step 3: Model Training
    success = run_script('run_train_model.py', 'Model Training')
    if not success:
        print("\n❌ Pipeline stopped due to error in model training")
        return
    
    # Success message
    print("\n" + "="*70)
    print(" "*20 + "🎉 PIPELINE COMPLETE! 🎉")
    print("="*70)
    print("\n✅ All steps completed successfully!")
    print("\n📂 Generated files:")
    print("   - data/f1_tyre_data.csv")
    print("   - data/f1_tyre_features.csv")
    print("   - data/track_characteristics.csv")
    print("   - model/tyre_recommender.pkl")
    print("   - model/scaler.pkl")
    print("   - model/label_encoder.pkl")
    print("   - model/feature_columns.pkl")
    
    print("\n🚀 Ready to run Streamlit app!")
    print("\n   Run: streamlit run app.py")
    print("="*70)

if __name__ == "__main__":
    main()
