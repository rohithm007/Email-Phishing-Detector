# Email Phishing Detection System 🛡️

A real-time email phishing detection system built with Python and Machine Learning. This system analyzes emails and identifies potential phishing attempts using a Random Forest classifier trained on various email features.

## 🌟 Features

- **Real-time Detection**: Analyze emails instantly through a REST API
- **Machine Learning**: Random Forest classifier with 20+ features
- **Feature Extraction**: Advanced analysis of URLs, keywords, sender information, and content patterns
- **Risk Levels**: Categorizes threats as SAFE, LOW, MEDIUM, HIGH, or CRITICAL
- **Batch Processing**: Analyze multiple emails at once
- **Easy to Use**: Simple API interface and command-line testing

## 📋 Features Analyzed

The system extracts and analyzes over 20 features including:

- **Sender Analysis**: Email validation, suspicious patterns, domain characteristics
- **Subject Analysis**: Urgency indicators, capitalization, exclamation marks
- **Content Analysis**: Phishing keywords, special character ratios, urgency score
- **URL Analysis**: Number of URLs, IP addresses, URL shorteners, mismatched links
- **HTML Analysis**: Forms, JavaScript, hidden elements
- **Statistical Features**: Length metrics, character distributions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
   ```powershell
   cd "d:\CyberProjects\email phissing detector"
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Train the model**
   ```powershell
   python train_model.py
   ```
   
   This will:
   - Load sample phishing and legitimate emails
   - Extract features from each email
   - Train a Random Forest classifier
   - Save the trained model to `models/phishing_detector.pkl`
   - Display training accuracy and feature importance

4. **Start the API server**
   ```powershell
   python app.py
   ```
   
   The API will be available at `http://localhost:5000`

## 📖 Usage

### Using the API

#### Detect Single Email

```powershell
# Using curl (if available) or Invoke-RestMethod
$body = @{
    subject = "URGENT: Verify your account"
    body = "Click here to verify your account: http://suspicious-link.com"
    sender = "alert@phishing-site.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/detect" -Method Post -Body $body -ContentType "application/json"
```

**Response:**
```json
{
  "email": {
    "subject": "URGENT: Verify your account",
    "sender": "alert@phishing-site.com"
  },
  "prediction": "PHISHING",
  "is_phishing": true,
  "confidence": 94.5,
  "risk_level": "CRITICAL",
  "recommendation": "⛔ DO NOT interact with this email. Delete immediately and report as phishing.",
  "features_analyzed": 23,
  "timestamp": "2025-11-04T12:30:45.123456"
}
```

#### Batch Detection

```python
import requests

emails = {
    "emails": [
        {
            "subject": "Team meeting notes",
            "body": "Here are the notes from today's meeting...",
            "sender": "manager@company.com"
        },
        {
            "subject": "URGENT: Account suspended!",
            "body": "Click here to reactivate: http://phish.com",
            "sender": "alert@suspicious.net"
        }
    ]
}

response = requests.post("http://localhost:5000/batch-detect", json=emails)
print(response.json())
```

### Using Python Directly

```python
from src.feature_extractor import EmailFeatureExtractor
from src.phishing_detector import PhishingDetector

# Initialize components
extractor = EmailFeatureExtractor()
detector = PhishingDetector()
detector.load_model()

# Analyze an email
email_data = {
    'subject': 'URGENT: Your account will be suspended',
    'body': 'Click here to verify: http://phishing-site.com',
    'sender': 'alert@suspicious.com'
}

features = extractor.extract_features(email_data)
result = detector.predict(features)

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence'] * 100:.2f}%")
print(f"Risk Level: {result['risk_level']}")
```

### Testing the System

Run the test script to validate the detection system:

```powershell
python test_detector.py
```

This will run several test cases and display:
- Predictions for each test email
- Confidence scores and risk levels
- Pass/fail status for each test
- Overall accuracy

## 🔌 API Endpoints

### `GET /`
Health check and API information
```json
{
  "service": "Email Phishing Detection API",
  "version": "1.0",
  "status": "running"
}
```

### `GET /health`
Check if the model is loaded and API is healthy
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### `POST /detect`
Analyze a single email for phishing

**Request Body:**
```json
{
  "subject": "Email subject",
  "body": "Email body content",
  "sender": "sender@example.com",
  "urls": ["http://example.com"]  // optional
}
```

**Response:**
```json
{
  "prediction": "PHISHING" | "LEGITIMATE",
  "is_phishing": true | false,
  "confidence": 85.3,
  "risk_level": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "SAFE",
  "recommendation": "Action recommendation",
  "features_analyzed": 23
}
```

### `POST /batch-detect`
Analyze multiple emails at once

**Request Body:**
```json
{
  "emails": [
    {
      "subject": "...",
      "body": "...",
      "sender": "..."
    }
  ]
}
```

### `GET /model/info`
Get model information and top features
```json
{
  "model_type": "Random Forest Classifier",
  "n_features": 23,
  "top_features": {
    "num_suspicious_keywords": 0.156,
    "urgency_score": 0.143,
    ...
  }
}
```

## 📁 Project Structure

```
email phissing detector/
├── src/
│   ├── feature_extractor.py    # Email feature extraction
│   └── phishing_detector.py    # ML model for detection
├── data/
│   └── sample_emails.py        # Sample training data
├── models/
│   └── phishing_detector.pkl   # Trained model (generated)
├── app.py                      # Flask API server
├── train_model.py              # Model training script
├── test_detector.py            # Testing script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎯 Risk Levels

- **CRITICAL** (≥80% confidence): Extremely likely phishing - Delete immediately
- **HIGH** (≥60% confidence): High risk - Verify sender carefully
- **MEDIUM** (≥40% confidence): Exercise caution
- **LOW** (≥20% confidence): Low risk but stay vigilant
- **SAFE** (<20% confidence): Appears legitimate

## 🔧 Customization

### Adding More Training Data

Edit `data/sample_emails.py` and add more emails to `PHISHING_EMAILS` or `LEGITIMATE_EMAILS`:

```python
PHISHING_EMAILS.append({
    'subject': 'Your subject',
    'body': 'Email body',
    'sender': 'sender@example.com',
    'label': 1  # 1 for phishing
})
```

Then retrain the model:
```powershell
python train_model.py
```

### Adjusting Model Parameters

Edit `src/phishing_detector.py` to modify the Random Forest parameters:

```python
self.model = RandomForestClassifier(
    n_estimators=100,      # Number of trees
    max_depth=20,          # Maximum tree depth
    min_samples_split=5,   # Minimum samples to split
    # ... more parameters
)
```

### Adding Custom Features

Add new feature extraction methods to `src/feature_extractor.py`:

```python
def _your_custom_feature(self, text):
    # Your feature logic here
    return value

# Then add to extract_features():
features['your_feature_name'] = self._your_custom_feature(body)
```

## 🧪 Example Test Cases

The system includes pre-configured test cases:

1. **Obvious Phishing**: Account suspension threats with urgent language
2. **Prize Scams**: Lottery winners and prize notifications
3. **Legitimate Work Emails**: Normal business communication
4. **Order Confirmations**: Legitimate transaction emails
5. **Mismatched URLs**: Links that don't match displayed text

## 📊 Model Performance

The trained model analyzes:
- **23 distinct features** per email
- **Random Forest** algorithm with 100 decision trees
- Features include URL analysis, keyword detection, sender validation, and content patterns

Top contributing features (typical):
1. Number of suspicious keywords
2. Urgency score
3. URL characteristics
4. Sender domain patterns
5. Subject line indicators

## 🛠️ Troubleshooting

**Model not loading?**
- Run `python train_model.py` to train the model first

**Import errors?**
- Install dependencies: `pip install -r requirements.txt`

**API not starting?**
- Check if port 5000 is available
- Try changing the port in `app.py`: `app.run(port=5001)`

**Low accuracy?**
- Add more training data to `data/sample_emails.py`
- Retrain the model with more diverse examples

## 🤝 Contributing

To improve the detection system:

1. Add more diverse training examples
2. Implement additional features (e.g., email headers, DKIM validation)
3. Experiment with different ML algorithms
4. Enhance the API with more endpoints

## 📝 License

This project is for educational purposes. Use responsibly and in compliance with applicable laws.

## ⚠️ Disclaimer

This tool is designed to assist in identifying potential phishing emails but should not be the only security measure. Always practice good email security habits:

- Verify sender identities independently
- Never click suspicious links
- Don't download unexpected attachments
- Report suspected phishing to your IT department

## 🚀 Future Enhancements

- [ ] Integration with email clients (IMAP/POP3)
- [ ] Real-time email header analysis
- [ ] Deep learning models (LSTM, BERT)
- [ ] Browser extension for Gmail/Outlook
- [ ] Automated reporting to security teams
- [ ] Visual dashboard for analytics
- [ ] Multi-language support

---

**Built with ❤️ using Python, scikit-learn, and Flask**
