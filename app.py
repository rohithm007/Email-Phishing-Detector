"""
Real-time Email Phishing Detection API
Flask REST API for detecting phishing emails in real-time
"""

from flask import Flask, request, jsonify
import sys
import os
import pandas as pd

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from feature_extractor import EmailFeatureExtractor
from phishing_detector import PhishingDetector

app = Flask(__name__)

# Initialize components
feature_extractor = EmailFeatureExtractor()
detector = PhishingDetector()

# Try to load pre-trained model
try:
    detector.load_model()
    print("✓ Pre-trained model loaded successfully")
except FileNotFoundError:
    print("⚠ No pre-trained model found. Please train the model first using train_model.py")


@app.route('/')
def home():
    """API home page"""
    return jsonify({
        'service': 'Email Phishing Detection API',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            '/detect': 'POST - Detect phishing in email',
            '/health': 'GET - Check API health',
            '/model/info': 'GET - Get model information'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    model_loaded = detector.model is not None
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded
    })


@app.route('/detect', methods=['POST'])
def detect_phishing():
    """
    Detect phishing in email
    
    Expected JSON payload:
    {
        "subject": "Email subject",
        "body": "Email body content",
        "sender": "sender@example.com",
        "urls": ["http://example.com"] (optional)
    }
    """
    try:
        # Check if model is loaded
        if detector.model is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.'
            }), 503
        
        # Get email data from request
        email_data = request.get_json()
        
        # Validate required fields
        if not email_data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        required_fields = ['subject', 'body', 'sender']
        missing_fields = [field for field in required_fields if field not in email_data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Extract features
        features = feature_extractor.extract_features(email_data)
        
        # Make prediction
        prediction = detector.predict(features)
        
        # Prepare response
        response = {
            'email': {
                'subject': email_data.get('subject', ''),
                'sender': email_data.get('sender', '')
            },
            'prediction': prediction['prediction'],
            'is_phishing': prediction['is_phishing'],
            'confidence': round(prediction['confidence'] * 100, 2),
            'risk_level': prediction['risk_level'],
            'recommendation': get_recommendation(prediction),
            'features_analyzed': len(features),
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/batch-detect', methods=['POST'])
def batch_detect():
    """
    Detect phishing in multiple emails
    
    Expected JSON payload:
    {
        "emails": [
            {
                "subject": "Email subject 1",
                "body": "Email body 1",
                "sender": "sender1@example.com"
            },
            ...
        ]
    }
    """
    try:
        if detector.model is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.'
            }), 503
        
        data = request.get_json()
        
        if not data or 'emails' not in data:
            return jsonify({'error': 'No emails provided'}), 400
        
        emails = data['emails']
        results = []
        
        for idx, email_data in enumerate(emails):
            try:
                features = feature_extractor.extract_features(email_data)
                prediction = detector.predict(features)
                
                results.append({
                    'index': idx,
                    'subject': email_data.get('subject', ''),
                    'prediction': prediction['prediction'],
                    'confidence': round(prediction['confidence'] * 100, 2),
                    'risk_level': prediction['risk_level']
                })
            except Exception as e:
                results.append({
                    'index': idx,
                    'error': str(e)
                })
        
        return jsonify({
            'total_emails': len(emails),
            'results': results
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information and feature importance"""
    try:
        if detector.model is None:
            return jsonify({
                'error': 'Model not loaded'
            }), 503
        
        feature_importance = detector.get_feature_importance()
        
        # Get top 10 most important features
        top_features = dict(list(feature_importance.items())[:10])
        
        return jsonify({
            'model_type': 'Random Forest Classifier',
            'n_features': len(feature_importance),
            'top_features': top_features,
            'model_loaded': True
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


def get_recommendation(prediction):
    """Get recommendation based on prediction"""
    if prediction['risk_level'] == 'CRITICAL':
        return "⛔ DO NOT interact with this email. Delete immediately and report as phishing."
    elif prediction['risk_level'] == 'HIGH':
        return "⚠️ High risk of phishing. Verify sender before taking any action."
    elif prediction['risk_level'] == 'MEDIUM':
        return "⚡ Exercise caution. Verify sender and don't click suspicious links."
    elif prediction['risk_level'] == 'LOW':
        return "✓ Low risk, but always verify before clicking links or downloading attachments."
    else:
        return "✅ Email appears safe, but always practice good email security."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
