# Email Notifications Setup Guide

This guide will help you set up email notifications for the Email Phishing Detection System.

## 📧 Gmail Setup (Recommended)

### Step 1: Enable 2-Step Verification

1. Go to your [Google Account](https://myaccount.google.com/)
2. Navigate to **Security** (left sidebar)
3. Under "Signing in to Google", click **2-Step Verification**
4. Follow the prompts to enable 2-Step Verification
5. Complete the setup process

### Step 2: Create App Password

1. Still in your Google Account, go to **Security**
2. Under "Signing in to Google", click **2-Step Verification**
3. Scroll down to the bottom and click **App passwords**
4. You may need to sign in again
5. In the "Select app" dropdown, choose **Mail**
6. In the "Select device" dropdown, choose **Windows Computer** (or your device)
7. Click **Generate**
8. Google will show you a 16-character password (e.g., `abcd efgh ijkl mnop`)
9. **Copy this password** - you'll use it in the `.env` file

### Step 3: Configure the Application

1. In your project directory, copy the example environment file:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Open the `.env` file in a text editor

3. Update the following values:
   ```env
   EMAIL_NOTIFICATIONS_ENABLED=true
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=abcdefghijklmnop  # Your 16-char App Password (no spaces)
   ADMIN_EMAIL=your-email@gmail.com  # Where alerts will be sent
   ```

   **Important Notes:**
   - Remove spaces from the App Password (e.g., `abcd efgh ijkl mnop` becomes `abcdefghijklmnop`)
   - `SENDER_EMAIL` is the Gmail account that will send the alerts
   - `ADMIN_EMAIL` is where you want to receive the phishing alerts (can be the same or different)

4. Save the `.env` file

### Step 4: Test the Configuration

1. Start the API server:
   ```powershell
   python app.py
   ```

2. Test the connection:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:5000/notifications/test"
   ```

   You should see:
   ```json
   {
     "status": "success",
     "message": "Successfully connected to smtp.gmail.com",
     "admin_email": "your-email@gmail.com"
   }
   ```

3. Send a test alert:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:5000/notifications/send-test" -Method Post
   ```

4. Check your email! You should receive a phishing alert.

## 📧 Other Email Providers

### Outlook/Hotmail

```env
EMAIL_NOTIFICATIONS_ENABLED=true
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SENDER_EMAIL=your-email@outlook.com
SENDER_PASSWORD=your-password
ADMIN_EMAIL=admin@outlook.com
```

**Note:** You may need to enable "Less secure app access" in your account settings.

### Yahoo Mail

```env
EMAIL_NOTIFICATIONS_ENABLED=true
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SENDER_EMAIL=your-email@yahoo.com
SENDER_PASSWORD=your-app-password
ADMIN_EMAIL=admin@yahoo.com
```

**Note:** Yahoo also requires an App Password. Generate it at: Account Info > Account Security > Generate app password

### Custom SMTP Server

```env
EMAIL_NOTIFICATIONS_ENABLED=true
SMTP_SERVER=mail.yourcompany.com
SMTP_PORT=587
SENDER_EMAIL=alerts@yourcompany.com
SENDER_PASSWORD=your-password
ADMIN_EMAIL=admin@yourcompany.com
```

## 🔧 Configuration Options

### Adjust Notification Threshold

By default, notifications are sent for phishing detections with ≥60% confidence. To change this, edit `src/email_notifier.py`:

```python
def send_phishing_alert(self, email_data, prediction_result):
    # Change this line to adjust threshold
    if prediction_result['confidence'] < 0.6:  # Change 0.6 to your preferred threshold
        return False
```

### Disable Notifications Temporarily

To disable notifications without removing your configuration:

```env
EMAIL_NOTIFICATIONS_ENABLED=false
```

### Send to Multiple Admins

Currently, alerts are sent to one admin email. To send to multiple recipients, edit `src/email_notifier.py`:

```python
# In the __init__ method:
self.admin_emails = os.getenv('ADMIN_EMAIL', '').split(',')

# In _create_alert_message:
message["To"] = ', '.join(self.admin_emails)
```

Then in `.env`:
```env
ADMIN_EMAIL=admin1@example.com,admin2@example.com,admin3@example.com
```

## 🐛 Troubleshooting

### "SMTP Authentication Error"

**Problem:** The app can't log in to your email account.

**Solutions:**
1. Verify your email and password are correct in `.env`
2. For Gmail: Make sure you're using an **App Password**, not your regular password
3. Check that 2-Step Verification is enabled
4. Remove any spaces from the App Password

### "Connection Refused" or "Timeout"

**Problem:** Can't connect to the SMTP server.

**Solutions:**
1. Check your internet connection
2. Verify `SMTP_SERVER` and `SMTP_PORT` are correct
3. Some networks block port 587 - try port 465 with SSL
4. Check your firewall settings

### No Email Received

**Problem:** Test succeeds but no email arrives.

**Solutions:**
1. Check your spam/junk folder
2. Verify `ADMIN_EMAIL` is correct
3. Wait a few minutes - some servers have delays
4. Check your email provider's settings for blocked senders

### "Notifications Disabled" Message

**Problem:** API says notifications are disabled.

**Solutions:**
1. Check that `EMAIL_NOTIFICATIONS_ENABLED=true` in your `.env` file
2. Make sure the `.env` file is in the project root directory
3. Restart the API server after changing `.env`
4. Verify all required fields are filled in `.env`

## 📧 Email Format Preview

When a phishing email is detected, the admin receives an email like this:

**Subject:** 🚨 PHISHING ALERT - HIGH Risk Detected

**Body:**
```
PHISHING EMAIL DETECTED
========================

Detection Time: 2025-11-05 14:30:45
Risk Level: HIGH
Confidence: 87.50%

EMAIL DETAILS:
--------------
From: alert@phishing-site.com
Subject: URGENT: Your account will be suspended

Body Preview:
Click here to verify your account immediately...

RECOMMENDATION:
⚠️ HIGH RISK: This email is highly suspicious. Verify the 
sender through an alternative communication channel before 
taking any action.
```

The HTML version includes color-coding, better formatting, and visual indicators for risk levels.

## 🔒 Security Best Practices

1. **Never commit `.env` file to version control** - It contains sensitive credentials
2. **Use App Passwords** - Never use your main email password
3. **Rotate passwords regularly** - Generate new App Passwords periodically
4. **Monitor admin inbox** - Regularly check for phishing alerts
5. **Test regularly** - Use the test endpoint to ensure notifications work
6. **Secure your server** - If deploying publicly, use HTTPS and authentication

## ✅ Quick Checklist

- [ ] 2-Step Verification enabled on Gmail
- [ ] App Password generated
- [ ] `.env` file created (copied from `.env.example`)
- [ ] All credentials filled in `.env`
- [ ] Spaces removed from App Password
- [ ] `EMAIL_NOTIFICATIONS_ENABLED=true`
- [ ] API server running
- [ ] Connection test successful (`/notifications/test`)
- [ ] Test alert received (`/notifications/send-test`)
- [ ] Checked spam folder if no email
- [ ] `.env` added to `.gitignore`

## 📞 Support

If you continue to have issues:

1. Check the console output when the API starts - it will show notification status
2. Review the error messages from the test endpoints
3. Verify your SMTP server settings with your email provider
4. Try sending a regular email from your account to verify it works

---

**Congratulations!** Once set up, you'll receive automatic alerts whenever high-confidence phishing emails are detected. 🎉
