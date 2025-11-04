"""
Email Feature Extractor for Phishing Detection
Extracts various features from email content and metadata
"""

import re
import tldextract
from urllib.parse import urlparse
from email_validator import validate_email, EmailNotValidError
from bs4 import BeautifulSoup
import string


class EmailFeatureExtractor:
    """Extract features from email for phishing detection"""
    
    # Common phishing keywords
    PHISHING_KEYWORDS = [
        'urgent', 'verify', 'confirm', 'suspend', 'restricted', 'update',
        'click here', 'login', 'account', 'password', 'credit card', 'bank',
        'security', 'alert', 'winner', 'prize', 'congratulations', 'claim',
        'verify your account', 'suspended', 'locked', 'unusual activity',
        'confirm your identity', 'gift card', 'refund', 'tax', 'inheritance'
    ]
    
    def __init__(self):
        self.features = {}
    
    def extract_features(self, email_data):
        """
        Extract all features from email data
        
        Args:
            email_data (dict): Dictionary containing email fields
                - subject: Email subject
                - body: Email body (text or HTML)
                - sender: Sender email address
                - urls: List of URLs in email (optional)
        
        Returns:
            dict: Dictionary of extracted features
        """
        subject = email_data.get('subject', '')
        body = email_data.get('body', '')
        sender = email_data.get('sender', '')
        urls = email_data.get('urls', [])
        
        # Extract text from HTML if necessary
        clean_body = self._clean_html(body)
        
        # Extract all URLs from body if not provided
        if not urls:
            urls = self._extract_urls(clean_body)
        
        features = {
            # Email length features
            'subject_length': len(subject),
            'body_length': len(clean_body),
            'num_words': len(clean_body.split()),
            
            # Sender features
            'sender_valid': self._is_valid_email(sender),
            'sender_has_numbers': int(bool(re.search(r'\d', sender))),
            'sender_domain_length': len(sender.split('@')[1]) if '@' in sender else 0,
            
            # Subject features
            'subject_has_urgent': int('urgent' in subject.lower()),
            'subject_all_caps': int(subject.isupper() and len(subject) > 3),
            'subject_exclamation': subject.count('!'),
            
            # Content features
            'num_urls': len(urls),
            'num_suspicious_keywords': self._count_phishing_keywords(subject + ' ' + clean_body),
            'has_ip_address': int(self._has_ip_address(urls)),
            'num_dots_in_url': self._count_dots_in_urls(urls),
            'num_external_links': len(urls),
            
            # Character analysis
            'special_char_ratio': self._special_char_ratio(clean_body),
            'digit_ratio': self._digit_ratio(clean_body),
            'uppercase_ratio': self._uppercase_ratio(clean_body),
            
            # Suspicious patterns
            'has_form': int('<form' in body.lower()),
            'has_javascript': int('<script' in body.lower()),
            'mismatched_url': self._check_mismatched_urls(body, urls),
            'shortened_url': int(any(self._is_shortened_url(url) for url in urls)),
            
            # Urgency indicators
            'urgency_score': self._calculate_urgency_score(subject + ' ' + clean_body),
        }
        
        return features
    
    def _clean_html(self, text):
        """Remove HTML tags and return clean text"""
        if '<html' in text.lower() or '<body' in text.lower():
            soup = BeautifulSoup(text, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return text
    
    def _extract_urls(self, text):
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    def _is_valid_email(self, email):
        """Check if email address is valid"""
        try:
            validate_email(email)
            return 1
        except EmailNotValidError:
            return 0
    
    def _count_phishing_keywords(self, text):
        """Count phishing-related keywords"""
        text_lower = text.lower()
        count = sum(1 for keyword in self.PHISHING_KEYWORDS if keyword in text_lower)
        return count
    
    def _has_ip_address(self, urls):
        """Check if any URL contains an IP address instead of domain"""
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        for url in urls:
            if re.search(ip_pattern, url):
                return True
        return False
    
    def _count_dots_in_urls(self, urls):
        """Count total dots in all URLs (subdomains can be suspicious)"""
        total_dots = 0
        for url in urls:
            try:
                parsed = urlparse(url)
                domain = parsed.netloc
                total_dots += domain.count('.')
            except:
                pass
        return total_dots
    
    def _special_char_ratio(self, text):
        """Calculate ratio of special characters"""
        if len(text) == 0:
            return 0
        special_chars = sum(1 for c in text if c in string.punctuation)
        return special_chars / len(text)
    
    def _digit_ratio(self, text):
        """Calculate ratio of digits"""
        if len(text) == 0:
            return 0
        digits = sum(1 for c in text if c.isdigit())
        return digits / len(text)
    
    def _uppercase_ratio(self, text):
        """Calculate ratio of uppercase letters"""
        if len(text) == 0:
            return 0
        uppercase = sum(1 for c in text if c.isupper())
        return uppercase / len(text)
    
    def _check_mismatched_urls(self, body, urls):
        """Check if displayed text doesn't match actual URL"""
        # Look for <a href="url">different text</a> patterns
        link_pattern = r'<a\s+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'
        matches = re.findall(link_pattern, body, re.IGNORECASE)
        
        mismatched = 0
        for href, text in matches:
            # If text looks like a URL but doesn't match href
            if 'http' in text.lower() and href.lower() not in text.lower():
                mismatched += 1
        
        return mismatched
    
    def _is_shortened_url(self, url):
        """Check if URL is from a URL shortening service"""
        shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 
                     'short.link', 'tiny.cc', 'is.gd', 'buff.ly']
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            return any(shortener in domain for shortener in shorteners)
        except:
            return False
    
    def _calculate_urgency_score(self, text):
        """Calculate urgency score based on urgent language"""
        urgency_words = ['urgent', 'immediate', 'act now', 'expires', 'limited time',
                        'hurry', 'quickly', 'don\'t wait', 'last chance', 'expire']
        text_lower = text.lower()
        score = sum(2 if word in text_lower else 0 for word in urgency_words)
        return min(score, 10)  # Cap at 10
