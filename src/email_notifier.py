"""
Email notification system for phishing detection alerts
Sends notifications to admin when phishing emails are detected
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EmailNotifier:
    """Send email notifications for phishing detections"""
    
    def __init__(self):
        """Initialize email notifier with credentials from environment variables"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.admin_email = os.getenv('ADMIN_EMAIL', '')
        self.enabled = os.getenv('EMAIL_NOTIFICATIONS_ENABLED', 'false').lower() == 'true'
        
        # Validate configuration
        if self.enabled and not all([self.sender_email, self.sender_password, self.admin_email]):
            print("⚠️ Warning: Email notifications enabled but credentials not configured properly")
            self.enabled = False
    
    def send_phishing_alert(self, email_data, prediction_result):
        """
        Send phishing alert to admin
        
        Args:
            email_data (dict): The email data that was analyzed
            prediction_result (dict): The prediction result from the detector
        
        Returns:
            bool: True if notification sent successfully, False otherwise
        """
        if not self.enabled:
            print("ℹ️ Email notifications are disabled")
            return False
        
        try:
            # Only send notification for high-risk detections
            if prediction_result['confidence'] < 0.6:
                print(f"ℹ️ Skipping notification - confidence too low ({prediction_result['confidence']*100:.1f}%)")
                return False
            
            # Create email message
            message = self._create_alert_message(email_data, prediction_result)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✅ Phishing alert sent to {self.admin_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ SMTP Authentication failed. Check your email credentials.")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Failed to send notification: {str(e)}")
            return False
    
    def _create_alert_message(self, email_data, prediction_result):
        """Create the alert email message"""
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🚨 PHISHING ALERT - {prediction_result['risk_level']} Risk Detected"
        message["From"] = self.sender_email
        message["To"] = self.admin_email
        
        # Create plain text version
        text_content = self._create_text_content(email_data, prediction_result)
        
        # Create HTML version
        html_content = self._create_html_content(email_data, prediction_result)
        
        # Attach both versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        
        message.attach(part1)
        message.attach(part2)
        
        return message
    
    def _create_text_content(self, email_data, prediction_result):
        """Create plain text email content"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        text = f"""
PHISHING EMAIL DETECTED
========================

Detection Time: {timestamp}
Risk Level: {prediction_result['risk_level']}
Confidence: {prediction_result['confidence']*100:.2f}%

EMAIL DETAILS:
--------------
From: {email_data.get('sender', 'N/A')}
Subject: {email_data.get('subject', 'N/A')}

Body Preview:
{email_data.get('body', 'N/A')[:200]}...

RECOMMENDATION:
{self._get_recommendation(prediction_result)}

---
This is an automated alert from the Email Phishing Detection System.
"""
        return text
    
    def _create_html_content(self, email_data, prediction_result):
        """Create HTML email content"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Color based on risk level
        risk_colors = {
            'CRITICAL': '#dc3545',
            'HIGH': '#fd7e14',
            'MEDIUM': '#ffc107',
            'LOW': '#0dcaf0',
            'SAFE': '#28a745'
        }
        risk_color = risk_colors.get(prediction_result['risk_level'], '#6c757d')
        
        html = f"""
        <html>
          <head>
            <style>
              body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
              .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
              .header {{ background-color: {risk_color}; color: white; padding: 20px; border-radius: 5px 5px 0 0; }}
              .content {{ background-color: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; }}
              .detail-row {{ margin: 10px 0; }}
              .label {{ font-weight: bold; color: #495057; }}
              .value {{ color: #212529; }}
              .footer {{ background-color: #e9ecef; padding: 10px; text-align: center; font-size: 12px; color: #6c757d; border-radius: 0 0 5px 5px; }}
              .risk-badge {{ display: inline-block; padding: 5px 10px; background-color: {risk_color}; color: white; border-radius: 3px; font-weight: bold; }}
              .email-preview {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid {risk_color}; }}
            </style>
          </head>
          <body>
            <div class="container">
              <div class="header">
                <h2>🚨 PHISHING EMAIL DETECTED</h2>
              </div>
              <div class="content">
                <div class="detail-row">
                  <span class="label">Detection Time:</span>
                  <span class="value">{timestamp}</span>
                </div>
                <div class="detail-row">
                  <span class="label">Risk Level:</span>
                  <span class="risk-badge">{prediction_result['risk_level']}</span>
                </div>
                <div class="detail-row">
                  <span class="label">Confidence:</span>
                  <span class="value">{prediction_result['confidence']*100:.2f}%</span>
                </div>
                
                <h3>Email Details</h3>
                <div class="detail-row">
                  <span class="label">From:</span>
                  <span class="value">{email_data.get('sender', 'N/A')}</span>
                </div>
                <div class="detail-row">
                  <span class="label">Subject:</span>
                  <span class="value">{email_data.get('subject', 'N/A')}</span>
                </div>
                
                <h3>Body Preview</h3>
                <div class="email-preview">
                  {email_data.get('body', 'N/A')[:300]}...
                </div>
                
                <h3>Recommendation</h3>
                <div class="email-preview">
                  {self._get_recommendation(prediction_result)}
                </div>
              </div>
              <div class="footer">
                This is an automated alert from the Email Phishing Detection System
              </div>
            </div>
          </body>
        </html>
        """
        return html
    
    def _get_recommendation(self, prediction_result):
        """Get recommendation based on risk level"""
        recommendations = {
            'CRITICAL': "⛔ IMMEDIATE ACTION REQUIRED: Delete this email immediately and report it to your security team. Do not click any links or download attachments.",
            'HIGH': "⚠️ HIGH RISK: This email is highly suspicious. Verify the sender through an alternative communication channel before taking any action.",
            'MEDIUM': "⚡ CAUTION ADVISED: Exercise extreme caution with this email. Verify all information before clicking links or providing any data.",
            'LOW': "✓ LOW RISK: While the risk is low, remain vigilant and verify sender authenticity before taking action.",
            'SAFE': "✅ This email appears safe, but always practice good email security habits."
        }
        return recommendations.get(prediction_result['risk_level'], "Review this email carefully.")
    
    def test_connection(self):
        """Test email configuration and connection"""
        if not self.enabled:
            return {
                'success': False,
                'message': 'Email notifications are disabled'
            }
        
        if not all([self.sender_email, self.sender_password, self.admin_email]):
            return {
                'success': False,
                'message': 'Email credentials not configured'
            }
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
            
            return {
                'success': True,
                'message': f'Successfully connected to {self.smtp_server}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection failed: {str(e)}'
            }
