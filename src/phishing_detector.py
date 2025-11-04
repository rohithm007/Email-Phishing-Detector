"""
Phishing Detection Model
Trains and uses ML model to detect phishing emails
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os


class PhishingDetector:
    """Machine Learning model for phishing email detection"""
    
    def __init__(self, model_path='models/phishing_detector.pkl'):
        self.model_path = model_path
        self.model = None
        self.feature_names = None
        
        # Load model if it exists
        if os.path.exists(model_path):
            self.load_model()
        else:
            # Initialize new Random Forest model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
    
    def train(self, X, y, test_size=0.2):
        """
        Train the phishing detection model
        
        Args:
            X: Feature matrix (DataFrame or array)
            y: Labels (0 = legitimate, 1 = phishing)
            test_size: Proportion of data for testing
        
        Returns:
            dict: Training metrics
        """
        # Convert to DataFrame if necessary
        if isinstance(X, dict):
            X = pd.DataFrame([X])
        
        # Store feature names
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
            X = X.values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Train model
        print("Training phishing detection model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred)
        }
        
        print(f"\nModel Accuracy: {metrics['accuracy']:.4f}")
        print("\nClassification Report:")
        print(metrics['classification_report'])
        
        return metrics
    
    def predict(self, features):
        """
        Predict if an email is phishing
        
        Args:
            features: Dictionary or array of email features
        
        Returns:
            dict: Prediction results with probability
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded. Train model first.")
        
        # Convert features to array
        if isinstance(features, dict):
            if self.feature_names:
                # Ensure features are in correct order
                feature_array = np.array([[features.get(name, 0) for name in self.feature_names]])
            else:
                feature_array = np.array([list(features.values())])
        else:
            feature_array = np.array([features])
        
        # Make prediction
        prediction = self.model.predict(feature_array)[0]
        probability = self.model.predict_proba(feature_array)[0]
        
        result = {
            'is_phishing': bool(prediction),
            'confidence': float(probability[1]),  # Probability of being phishing
            'risk_level': self._get_risk_level(probability[1]),
            'prediction': 'PHISHING' if prediction == 1 else 'LEGITIMATE'
        }
        
        return result
    
    def _get_risk_level(self, phishing_probability):
        """Determine risk level based on probability"""
        if phishing_probability >= 0.8:
            return 'CRITICAL'
        elif phishing_probability >= 0.6:
            return 'HIGH'
        elif phishing_probability >= 0.4:
            return 'MEDIUM'
        elif phishing_probability >= 0.2:
            return 'LOW'
        else:
            return 'SAFE'
    
    def save_model(self, path=None):
        """Save trained model to disk"""
        if path is None:
            path = self.model_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save model and feature names
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, path)
        print(f"Model saved to {path}")
    
    def load_model(self, path=None):
        """Load trained model from disk"""
        if path is None:
            path = self.model_path
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        
        model_data = joblib.load(path)
        self.model = model_data['model']
        self.feature_names = model_data.get('feature_names')
        print(f"Model loaded from {path}")
    
    def get_feature_importance(self):
        """Get feature importance scores"""
        if self.model is None:
            raise ValueError("Model not trained or loaded.")
        
        importances = self.model.feature_importances_
        
        if self.feature_names:
            feature_importance = dict(zip(self.feature_names, importances))
            # Sort by importance
            feature_importance = dict(sorted(feature_importance.items(), 
                                            key=lambda x: x[1], 
                                            reverse=True))
        else:
            feature_importance = {f'feature_{i}': imp 
                                 for i, imp in enumerate(importances)}
        
        return feature_importance
