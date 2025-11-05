"""
Train the phishing detection model using sample data
"""

import sys
import os
import pandas as pd
import numpy as np

from src.feature_extractor import EmailFeatureExtractor
from src.phishing_detector import PhishingDetector
from data.sample_emails import get_training_data


def train_model():
    """Train the phishing detection model"""
    print("=" * 60)
    print("EMAIL PHISHING DETECTION - Model Training")
    print("=" * 60)
    
    # Initialize components
    extractor = EmailFeatureExtractor()
    detector = PhishingDetector()
    
    # Load training data
    print("\n[1/4] Loading training data...")
    emails = get_training_data()
    print(f"✓ Loaded {len(emails)} email samples")
    
    # Extract features from all emails
    print("\n[2/4] Extracting features from emails...")
    features_list = []
    labels = []
    
    for email in emails:
        features = extractor.extract_features(email)
        features_list.append(features)
        labels.append(email['label'])
    
    # Convert to DataFrame
    X = pd.DataFrame(features_list)
    y = np.array(labels)
    
    print(f"✓ Extracted {len(X.columns)} features from each email")
    print(f"  - Phishing emails: {sum(y == 1)}")
    print(f"  - Legitimate emails: {sum(y == 0)}")
    
    # Display some feature names
    print(f"\nFeature examples: {', '.join(X.columns[:5].tolist())}...")
    
    # Train model
    print("\n[3/4] Training Random Forest model...")
    metrics = detector.train(X, y, test_size=0.25)
    
    # Save model
    print("\n[4/4] Saving trained model...")
    detector.save_model()
    
    # Display feature importance
    print("\n" + "=" * 60)
    print("TOP 10 MOST IMPORTANT FEATURES")
    print("=" * 60)
    feature_importance = detector.get_feature_importance()
    for i, (feature, importance) in enumerate(list(feature_importance.items())[:10], 1):
        print(f"{i:2d}. {feature:30s} {importance:.4f}")
    
    print("\n" + "=" * 60)
    print("✓ Model training completed successfully!")
    print("=" * 60)
    print("\nThe model is now ready to use for real-time phishing detection.")
    print("Run 'python app.py' to start the API server.\n")


if __name__ == '__main__':
    train_model()
