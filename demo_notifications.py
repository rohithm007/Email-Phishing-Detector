"""
Demo script showing email notification feature
Tests the phishing detection with notification alerts
"""

import requests
import json

API_URL = "http://localhost:5000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_notification_config():
    """Test if notifications are configured"""
    print_section("Testing Email Notification Configuration")
    
    try:
        response = requests.get(f"{API_URL}/notifications/test")
        result = response.json()
        
        if result['status'] == 'success':
            print("✅ Email notifications are properly configured!")
            print(f"   SMTP Server: {result['smtp_server']}")
            print(f"   Admin Email: {result['admin_email']}")
            return True
        else:
            print("❌ Email notifications not configured")
            print(f"   Message: {result['message']}")
            print("\nTo enable notifications:")
            print("1. Copy .env.example to .env")
            print("2. Fill in your email credentials")
            print("3. Set EMAIL_NOTIFICATIONS_ENABLED=true")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running?")
        print("   Start it with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def send_test_alert():
    """Send a test phishing alert"""
    print_section("Sending Test Phishing Alert")
    
    try:
        response = requests.post(f"{API_URL}/notifications/send-test")
        result = response.json()
        
        if result['status'] == 'success':
            print("✅ Test alert sent successfully!")
            print(f"   {result['message']}")
            print("\n📧 Check your inbox for the phishing alert email")
        else:
            print("❌ Failed to send test alert")
            print(f"   {result['message']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_phishing_detection_with_notification():
    """Test phishing detection and notification"""
    print_section("Testing Phishing Detection with Notifications")
    
    # High-risk phishing email
    phishing_email = {
        "subject": "URGENT: Your account has been suspended!",
        "body": "Dear user, Your account shows unusual activity. Click here immediately to verify your identity or your account will be permanently locked: http://suspicious-bank-verify.tk/login",
        "sender": "security@bank-alert123.com"
    }
    
    print("\n📨 Testing with suspicious email:")
    print(f"   From: {phishing_email['sender']}")
    print(f"   Subject: {phishing_email['subject']}")
    
    try:
        response = requests.post(f"{API_URL}/detect", json=phishing_email)
        result = response.json()
        
        print(f"\n🤖 Detection Result:")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Risk Level: {result['risk_level']}")
        
        if result.get('notification_sent', False):
            print(f"\n✅ Notification sent to admin!")
            print(f"   📧 Check your email for the phishing alert")
        else:
            print(f"\nℹ️ No notification sent")
            if result['confidence'] < 60:
                print(f"   (Confidence {result['confidence']}% is below 60% threshold)")
            else:
                print(f"   (Email notifications may be disabled)")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_legitimate_email():
    """Test with legitimate email (should not trigger notification)"""
    print_section("Testing Legitimate Email (No Notification Expected)")
    
    legitimate_email = {
        "subject": "Team meeting notes - November 5",
        "body": "Hi team, Here are the notes from today's meeting. Please review and let me know if I missed anything. Thanks!",
        "sender": "manager@company.com"
    }
    
    print("\n📨 Testing with legitimate email:")
    print(f"   From: {legitimate_email['sender']}")
    print(f"   Subject: {legitimate_email['subject']}")
    
    try:
        response = requests.post(f"{API_URL}/detect", json=legitimate_email)
        result = response.json()
        
        print(f"\n🤖 Detection Result:")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Confidence: {result['confidence']}%")
        print(f"   Risk Level: {result['risk_level']}")
        
        if result.get('notification_sent', False):
            print(f"\n⚠️ Unexpected: Notification was sent")
        else:
            print(f"\n✅ Correctly identified as legitimate - No notification sent")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main demo function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     EMAIL PHISHING DETECTION - NOTIFICATION DEMO            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Test 1: Check configuration
    config_ok = test_notification_config()
    
    if not config_ok:
        print("\n⚠️ Continuing with demo, but notifications won't be sent.")
        print("   See EMAIL_NOTIFICATIONS_SETUP.md for setup instructions.\n")
        input("Press Enter to continue...")
    
    # Test 2: Send test alert (if configured)
    if config_ok:
        input("\nPress Enter to send test alert...")
        send_test_alert()
    
    # Test 3: Detect phishing with notification
    input("\nPress Enter to test phishing detection...")
    test_phishing_detection_with_notification()
    
    # Test 4: Legitimate email (no notification)
    input("\nPress Enter to test legitimate email...")
    test_legitimate_email()
    
    # Summary
    print_section("Demo Complete!")
    print("""
    What you've seen:
    
    ✅ Email notification configuration test
    ✅ Test phishing alert sent to admin
    ✅ Automatic notification when phishing detected (≥60% confidence)
    ✅ No notification for legitimate emails
    
    Next Steps:
    
    1. Check your admin email inbox for alerts
    2. Review the phishing alert format (HTML + text)
    3. Configure .env file if notifications are disabled
    4. Integrate this into your email monitoring system
    
    For setup instructions, see: EMAIL_NOTIFICATIONS_SETUP.md
    """)

if __name__ == '__main__':
    main()
