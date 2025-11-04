"""
Test the phishing detection system
Run various test cases to validate the model
"""

import sys
import os
import requests
import json

# Test if running API or direct model
USE_API = False  # Set to True to test API, False to test model directly

if not USE_API:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from feature_extractor import EmailFeatureExtractor
    from phishing_detector import PhishingDetector


# Test cases
TEST_EMAILS = [
    {
        'name': 'Obvious Phishing - Account Suspension',
        'email': {
            'subject': 'URGENT: Account will be suspended in 24 hours!',
            'body': 'Your PayPal account shows suspicious activity. Click here immediately to verify: http://paypal-verify.tk/login',
            'sender': 'security@paypa1-alert.com'
        },
        'expected': 'PHISHING'
    },
    {
        'name': 'Obvious Phishing - Prize Winner',
        'email': {
            'subject': 'Congratulations! You won!',
            'body': 'You are our lucky winner! Claim $10,000 now by providing your bank details. Act fast! http://bit.ly/win123',
            'sender': 'winner@lottery-prize.net'
        },
        'expected': 'PHISHING'
    },
    {
        'name': 'Legitimate - Work Email',
        'email': {
            'subject': 'Team meeting tomorrow at 10 AM',
            'body': 'Hi team, Just a reminder about our weekly sync tomorrow at 10 AM. Please review the agenda I shared yesterday. Thanks!',
            'sender': 'manager@mycompany.com'
        },
        'expected': 'LEGITIMATE'
    },
    {
        'name': 'Legitimate - Order Confirmation',
        'email': {
            'subject': 'Your Amazon order has shipped',
            'body': 'Thank you for your order! Your package will arrive by Thursday. Track it here: https://www.amazon.com/tracking/ABC123',
            'sender': 'auto-confirm@amazon.com'
        },
        'expected': 'LEGITIMATE'
    },
    {
        'name': 'Suspicious - Mismatched URL',
        'email': {
            'subject': 'Security Alert from Your Bank',
            'body': 'Dear customer, unusual activity detected. Please login at <a href="http://fake-bank.ru">https://yourbank.com</a> to verify.',
            'sender': 'alerts@yourbank.com'
        },
        'expected': 'PHISHING'
    },
]


def test_with_api():
    """Test using the API endpoint"""
    API_URL = 'http://localhost:5000/detect'
    
    print("=" * 70)
    print("TESTING PHISHING DETECTION API")
    print("=" * 70)
    
    # Check API health
    try:
        response = requests.get('http://localhost:5000/health')
        health = response.json()
        print(f"\n✓ API Status: {health['status']}")
        print(f"✓ Model Loaded: {health['model_loaded']}\n")
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API.")
        print("  Please start the API server first: python app.py\n")
        return
    
    results = []
    
    for i, test in enumerate(TEST_EMAILS, 1):
        print(f"\n[Test {i}/{len(TEST_EMAILS)}] {test['name']}")
        print("-" * 70)
        
        try:
            response = requests.post(API_URL, json=test['email'])
            result = response.json()
            
            prediction = result['prediction']
            confidence = result['confidence']
            risk_level = result['risk_level']
            
            # Check if prediction matches expected
            correct = prediction == test['expected']
            status = "✓ PASS" if correct else "✗ FAIL"
            
            print(f"Subject: {test['email']['subject'][:50]}...")
            print(f"Prediction: {prediction} (Confidence: {confidence}%)")
            print(f"Risk Level: {risk_level}")
            print(f"Expected: {test['expected']}")
            print(f"Result: {status}")
            
            results.append(correct)
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    print(f"Accuracy: {sum(results)/len(results)*100:.1f}%")
    print("=" * 70 + "\n")


def test_with_model():
    """Test using the model directly"""
    print("=" * 70)
    print("TESTING PHISHING DETECTION MODEL (Direct)")
    print("=" * 70)
    
    # Initialize components
    try:
        extractor = EmailFeatureExtractor()
        detector = PhishingDetector()
        detector.load_model()
        print("\n✓ Model loaded successfully\n")
    except FileNotFoundError:
        print("\n✗ Error: Model not found.")
        print("  Please train the model first: python train_model.py\n")
        return
    
    results = []
    
    for i, test in enumerate(TEST_EMAILS, 1):
        print(f"\n[Test {i}/{len(TEST_EMAILS)}] {test['name']}")
        print("-" * 70)
        
        try:
            # Extract features
            features = extractor.extract_features(test['email'])
            
            # Make prediction
            result = detector.predict(features)
            
            prediction = result['prediction']
            confidence = result['confidence'] * 100
            risk_level = result['risk_level']
            
            # Check if prediction matches expected
            correct = prediction == test['expected']
            status = "✓ PASS" if correct else "✗ FAIL"
            
            print(f"Subject: {test['email']['subject'][:50]}...")
            print(f"Prediction: {prediction} (Confidence: {confidence:.2f}%)")
            print(f"Risk Level: {risk_level}")
            print(f"Expected: {test['expected']}")
            print(f"Result: {status}")
            
            results.append(correct)
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    print(f"Accuracy: {sum(results)/len(results)*100:.1f}%")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    if USE_API:
        test_with_api()
    else:
        test_with_model()
