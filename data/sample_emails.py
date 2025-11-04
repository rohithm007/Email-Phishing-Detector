"""
Sample dataset for training phishing detection model
"""

# Sample phishing emails
PHISHING_EMAILS = [
    {
        'subject': 'URGENT: Your account will be suspended!',
        'body': 'Dear user, Your account shows unusual activity. Click here immediately to verify your identity or your account will be locked within 24 hours. http://suspicious-bank-verify.com/login',
        'sender': 'security@b4nk-alert123.com',
        'label': 1
    },
    {
        'subject': 'Congratulations! You won $1,000,000',
        'body': 'You have been selected as our lucky winner! Claim your prize now by clicking this link and entering your bank details. Limited time offer! http://192.168.1.100/claim',
        'sender': 'prizes2024@winner-notification.net',
        'label': 1
    },
    {
        'subject': 'Verify your Netflix account NOW',
        'body': 'Your Netflix subscription has expired. Update your payment information immediately to avoid service interruption. Click here: http://netflix-verify.tk/update',
        'sender': 'no-reply@netflix-billing99.com',
        'label': 1
    },
    {
        'subject': 'Your tax refund is ready',
        'body': 'The IRS has approved your tax refund of $2,847. Click here to claim your refund immediately: http://irs-refund.short.link/claim. You must act within 48 hours.',
        'sender': 'refunds@irs-treasury.info',
        'label': 1
    },
    {
        'subject': 'Action Required: Confirm your email',
        'body': 'Dear customer, We detected suspicious login from unknown location. Verify your account now to prevent suspension. Click: http://bit.ly/3xYz9pQ',
        'sender': 'security-team@paypa1-secure.com',
        'label': 1
    },
    {
        'subject': 'FINAL NOTICE - Account Locked',
        'body': 'YOUR ACCOUNT HAS BEEN LOCKED DUE TO SECURITY BREACH! Immediate action required. Update password here: http://account-recovery.herokuapp.com/reset',
        'sender': 'alert@security-microsoft.com',
        'label': 1
    },
    {
        'subject': 'You have received an inheritance',
        'body': 'Dear Sir/Madam, I am writing to inform you of an inheritance of $5.8 million from a distant relative. Please provide your bank account details to process the transfer.',
        'sender': 'lawyer@inheritance-claims.biz',
        'label': 1
    },
    {
        'subject': 'Amazon: Unusual sign-in attempt',
        'body': 'We noticed a sign-in attempt from Nigeria. If this wasnt you, click here to secure your account urgently: http://amazon-security123.com/verify Your account will be suspended if you dont act now.',
        'sender': 'no-reply@amazon-alerts.co',
        'label': 1
    },
    {
        'subject': 'Your package could not be delivered',
        'body': 'Your DHL package #DHL837462 could not be delivered. Update your address information here: http://dhl-tracking.online/update Failure to do so will result in package return.',
        'sender': 'tracking@dhl-delivery.net',
        'label': 1
    },
    {
        'subject': 'Confirm your credit card details',
        'body': 'Dear valued customer, For security purposes, please confirm your credit card information by clicking the link below. Your card will be deactivated if not confirmed within 24 hours. http://bank-verify-secure.com',
        'sender': 'security@credit-card-services.info',
        'label': 1
    },
]

# Sample legitimate emails
LEGITIMATE_EMAILS = [
    {
        'subject': 'Weekly Team Meeting Notes - Nov 4',
        'body': 'Hi team, Here are the notes from today\'s meeting: 1. Project timeline discussed, 2. New feature requirements gathered, 3. Next meeting scheduled for Nov 11. Please review and let me know if I missed anything.',
        'sender': 'manager@mycompany.com',
        'label': 0
    },
    {
        'subject': 'Your order #12345 has shipped',
        'body': 'Thank you for your order! Your package is on the way and should arrive by Friday. Track your shipment here: https://www.amazon.com/tracking/12345. Order details are attached.',
        'sender': 'auto-confirm@amazon.com',
        'label': 0
    },
    {
        'subject': 'Quarterly Newsletter - Company Updates',
        'body': 'Dear colleagues, We are excited to share our Q3 achievements and upcoming initiatives. Read about our new product launches, team expansions, and upcoming events in this newsletter.',
        'sender': 'communications@techcorp.com',
        'label': 0
    },
    {
        'subject': 'Meeting Invitation: Project Review',
        'body': 'You are invited to the project review meeting on November 10 at 2:00 PM. Location: Conference Room B. Agenda: Review milestones, discuss blockers, plan next sprint.',
        'sender': 'calendar@company.com',
        'label': 0
    },
    {
        'subject': 'Your LinkedIn connection request',
        'body': 'John Smith accepted your connection request. Stay connected with John and others in your network. View John\'s profile: https://www.linkedin.com/in/johnsmith',
        'sender': 'notifications@linkedin.com',
        'label': 0
    },
    {
        'subject': 'Invoice for November Services',
        'body': 'Dear valued customer, Please find attached your invoice for services rendered in November 2025. Amount due: $250.00. Payment due by Nov 30. Thank you for your business.',
        'sender': 'billing@cloudservices.com',
        'label': 0
    },
    {
        'subject': 'GitHub: New pull request in your repository',
        'body': 'Alice opened a pull request in your repository "project-name". Title: "Add user authentication feature". View the changes and review the code on GitHub.',
        'sender': 'notifications@github.com',
        'label': 0
    },
    {
        'subject': 'Welcome to our service!',
        'body': 'Thank you for signing up! We are excited to have you on board. Get started by completing your profile and exploring our features. If you have questions, our support team is here to help.',
        'sender': 'welcome@newservice.com',
        'label': 0
    },
    {
        'subject': 'Your appointment confirmation',
        'body': 'This is to confirm your appointment on November 15, 2025 at 10:00 AM with Dr. Johnson. Location: Medical Center, 123 Health St. Please arrive 15 minutes early.',
        'sender': 'appointments@healthclinic.org',
        'label': 0
    },
    {
        'subject': 'Password reset successful',
        'body': 'Your password has been successfully reset. If you did not make this change, please contact our security team immediately at security@company.com or call 1-800-SECURITY.',
        'sender': 'security@trustedcompany.com',
        'label': 0
    },
]

def get_training_data():
    """Get all training data as list"""
    return PHISHING_EMAILS + LEGITIMATE_EMAILS

def get_phishing_emails():
    """Get only phishing emails"""
    return PHISHING_EMAILS

def get_legitimate_emails():
    """Get only legitimate emails"""
    return LEGITIMATE_EMAILS
