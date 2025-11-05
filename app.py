"""
Real-time Email Phishing Detection API
Flask REST API for detecting phishing emails in real-time
"""

from flask import Flask, request, jsonify
import sys
import os
import pandas as pd

from src.feature_extractor import EmailFeatureExtractor
from src.phishing_detector import PhishingDetector
from src.email_notifier import EmailNotifier

app = Flask(__name__)

# Initialize components
feature_extractor = EmailFeatureExtractor()
detector = PhishingDetector()
notifier = EmailNotifier()

# Try to load pre-trained model
try:
    detector.load_model()
    print("✓ Pre-trained model loaded successfully")
except FileNotFoundError:
    print("⚠ No pre-trained model found. Please train the model first using train_model.py")

# Check email notification status
if notifier.enabled:
    print(f"✓ Email notifications enabled - Admin: {notifier.admin_email}")
else:
    print("ℹ️ Email notifications disabled (configure .env to enable)")


@app.route('/')
def home():
    """API home page"""
    return jsonify({
        'service': 'Email Phishing Detection API',
        'version': '1.0',
        'status': 'running',
        'notifications_enabled': notifier.enabled,
        'endpoints': {
            '/detect': 'POST - Detect phishing in email',
            '/batch-detect': 'POST - Detect phishing in multiple emails',
            '/health': 'GET - Check API health',
            '/model/info': 'GET - Get model information',
            '/notifications/test': 'GET - Test notification configuration',
            '/notifications/send-test': 'POST - Send test phishing alert'
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
        
        # Send notification if phishing detected
        notification_sent = False
        if prediction['is_phishing']:
            notification_sent = notifier.send_phishing_alert(email_data, prediction)
        
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
            'notification_sent': notification_sent,
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


@app.route('/notifications/test', methods=['GET'])
def test_notifications():
    """Test email notification configuration"""
    result = notifier.test_connection()
    
    if result['success']:
        return jsonify({
            'status': 'success',
            'message': result['message'],
            'admin_email': notifier.admin_email,
            'smtp_server': notifier.smtp_server
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': result['message']
        }), 400


@app.route('/notifications/send-test', methods=['POST'])
def send_test_notification():
    """Send a test phishing alert"""
    test_email = {
        'subject': 'TEST: Phishing Detection Alert',
        'body': 'This is a test email to verify the notification system is working correctly.',
        'sender': 'test@example.com'
    }
    
    test_prediction = {
        'is_phishing': True,
        'confidence': 0.95,
        'risk_level': 'CRITICAL',
        'prediction': 'PHISHING'
    }
    
    success = notifier.send_phishing_alert(test_email, test_prediction)
    
    if success:
        return jsonify({
            'status': 'success',
            'message': f'Test alert sent to {notifier.admin_email}'
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to send test alert. Check configuration.'
        }), 400


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
