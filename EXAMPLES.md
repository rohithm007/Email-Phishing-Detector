# Email Phishing Detection - Example Usage

## Python Script Examples

### Example 1: Basic Email Analysis

```python
from src.feature_extractor import EmailFeatureExtractor
from src.phishing_detector import PhishingDetector

# Initialize
extractor = EmailFeatureExtractor()
detector = PhishingDetector()
detector.load_model()

# Email to analyze
email = {
    'subject': 'URGENT: Your account will be suspended!',
    'body': 'Click here to verify your identity immediately: http://phishing-site.tk',
    'sender': 'security@fake-bank.com'
}

# Extract features and predict
features = extractor.extract_features(email)
result = detector.predict(features)

# Display results
print(f"Email Subject: {email['subject']}")
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence'] * 100:.2f}%")
print(f"Risk Level: {result['risk_level']}")
```

### Example 2: Batch Analysis

```python
from src.feature_extractor import EmailFeatureExtractor
from src.phishing_detector import PhishingDetector

extractor = EmailFeatureExtractor()
detector = PhishingDetector()
detector.load_model()

emails = [
    {
        'subject': 'Meeting tomorrow',
        'body': 'Hi team, reminder about our meeting at 10 AM.',
        'sender': 'manager@company.com'
    },
    {
        'subject': 'Win $10,000 NOW!',
        'body': 'Click to claim your prize: http://scam.com',
        'sender': 'prizes@lottery.net'
    }
]

for i, email in enumerate(emails, 1):
    features = extractor.extract_features(email)
    result = detector.predict(features)
    print(f"\nEmail {i}: {result['prediction']} ({result['confidence']*100:.1f}%)")
```

## API Examples

### PowerShell Examples

```powershell
# Test single email
$email = @{
    subject = "URGENT: Verify your account"
    body = "Click here: http://phishing-link.com"
    sender = "alert@suspicious.net"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/detect" `
                  -Method Post `
                  -Body $email `
                  -ContentType "application/json"
```

### Python Requests Examples

```python
import requests

# Single email detection
url = "http://localhost:5000/detect"

email_data = {
    "subject": "Your package could not be delivered",
    "body": "Update your address here: http://fake-delivery.com",
    "sender": "delivery@scam.net"
}

response = requests.post(url, json=email_data)
result = response.json()

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}%")
print(f"Risk Level: {result['risk_level']}")
print(f"Recommendation: {result['recommendation']}")
```

### cURL Example

```bash
curl -X POST http://localhost:5000/detect \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "URGENT: Action required",
    "body": "Your account will be suspended. Click here to verify.",
    "sender": "alert@phishing.com"
  }'
```

## Real-World Scenarios

### Scenario 1: Email Client Integration

```python
import imaplib
import email
from src.feature_extractor import EmailFeatureExtractor
from src.phishing_detector import PhishingDetector

def scan_inbox(email_address, password):
    """Scan inbox for phishing emails"""
    
    extractor = EmailFeatureExtractor()
    detector = PhishingDetector()
    detector.load_model()
    
    # Connect to email (example with Gmail)
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, password)
    mail.select('inbox')
    
    # Search for recent emails
    _, message_numbers = mail.search(None, 'UNSEEN')
    
    phishing_found = []
    
    for num in message_numbers[0].split():
        _, msg_data = mail.fetch(num, '(RFC822)')
        email_body = msg_data[0][1]
        message = email.message_from_bytes(email_body)
        
        # Analyze email
        email_data = {
            'subject': message['subject'],
            'body': str(message.get_payload()),
            'sender': message['from']
        }
        
        features = extractor.extract_features(email_data)
        result = detector.predict(features)
        
        if result['is_phishing'] and result['confidence'] > 0.7:
            phishing_found.append({
                'subject': email_data['subject'],
                'sender': email_data['sender'],
                'confidence': result['confidence']
            })
    
    mail.close()
    mail.logout()
    
    return phishing_found

# Usage
# phishing = scan_inbox('your@email.com', 'your_app_password')
# for email in phishing:
#     print(f"⚠️ Phishing detected: {email['subject']}")
```

### Scenario 2: Automated Monitoring Service

```python
import time
import requests
from datetime import datetime

def monitor_emails(check_interval=60):
    """Monitor and log phishing detections"""
    
    print(f"Starting email monitoring (checking every {check_interval}s)")
    
    while True:
        # Get emails to check (from your email service/database)
        emails_to_check = get_new_emails()  # Your function
        
        for email in emails_to_check:
            response = requests.post(
                'http://localhost:5000/detect',
                json=email
            )
            
            result = response.json()
            
            if result['is_phishing'] and result['confidence'] > 70:
                # Log the phishing attempt
                log_phishing_attempt(email, result)
                # Alert security team
                send_alert(email, result)
        
        time.sleep(check_interval)

def log_phishing_attempt(email, result):
    """Log phishing detection to file"""
    timestamp = datetime.now().isoformat()
    with open('phishing_log.txt', 'a') as f:
        f.write(f"{timestamp} | {result['risk_level']} | "
                f"{email['sender']} | {email['subject']}\n")

def send_alert(email, result):
    """Send alert to security team"""
    print(f"🚨 ALERT: Phishing detected!")
    print(f"   From: {email['sender']}")
    print(f"   Subject: {email['subject']}")
    print(f"   Confidence: {result['confidence']}%")
```

### Scenario 3: Web Dashboard

```python
from flask import Flask, render_template, request, jsonify
from src.feature_extractor import EmailFeatureExtractor
from src.phishing_detector import PhishingDetector

app = Flask(__name__)
extractor = EmailFeatureExtractor()
detector = PhishingDetector()
detector.load_model()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    email_data = request.form.to_dict()
    features = extractor.extract_features(email_data)
    result = detector.predict(features)
    
    return jsonify({
        'prediction': result['prediction'],
        'confidence': f"{result['confidence'] * 100:.1f}%",
        'risk_level': result['risk_level'],
        'features': features
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
```

## Testing Different Email Types

### Phishing Email Examples

```python
# Account verification phishing
phishing_1 = {
    'subject': 'Urgent: Verify Your Account',
    'body': 'Your account has been locked. Verify now: http://fake-bank.tk',
    'sender': 'security@bank-alert.net'
}

# Prize scam
phishing_2 = {
    'subject': 'You Won $100,000!!!',
    'body': 'Claim your prize now! Limited time! http://bit.ly/scam123',
    'sender': 'winner@lottery-prize.com'
}

# Invoice scam
phishing_3 = {
    'subject': 'Invoice #12345 - Payment Required',
    'body': 'Please pay the attached invoice immediately. Download: http://malware.com/invoice.exe',
    'sender': 'billing@fake-company.biz'
}
```

### Legitimate Email Examples

```python
# Work email
legitimate_1 = {
    'subject': 'Project Update - Q4 Review',
    'body': 'Team, please review the Q4 project status document attached.',
    'sender': 'pm@yourcompany.com'
}

# Newsletter
legitimate_2 = {
    'subject': 'Monthly Newsletter - November 2025',
    'body': 'Here are this month\'s highlights and upcoming events...',
    'sender': 'newsletter@company.com'
}

# Order confirmation
legitimate_3 = {
    'subject': 'Order Confirmation #987654',
    'body': 'Thank you for your order. Track shipment: https://amazon.com/track/987654',
    'sender': 'auto-confirm@amazon.com'
}
```

## Performance Tips

### 1. Batch Processing for Efficiency

```python
# Process multiple emails efficiently
emails = [email1, email2, email3, ...]  # Your emails

features_list = [extractor.extract_features(e) for e in emails]
results = [detector.predict(f) for f in features_list]

# Filter high-risk emails
high_risk = [
    (emails[i], results[i]) 
    for i in range(len(emails)) 
    if results[i]['confidence'] > 0.8
]
```

### 2. Caching for Repeated Checks

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_predict(email_hash):
    """Cache predictions for identical emails"""
    # Your prediction logic
    pass
```

### 3. Async Processing

```python
import asyncio
import aiohttp

async def analyze_email_async(session, email):
    async with session.post('http://localhost:5000/detect', json=email) as resp:
        return await resp.json()

async def batch_analyze_async(emails):
    async with aiohttp.ClientSession() as session:
        tasks = [analyze_email_async(session, email) for email in emails]
        return await asyncio.gather(*tasks)

# Usage
# results = asyncio.run(batch_analyze_async(email_list))
```
