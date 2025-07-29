# src/atchatbot/parser.py
"""
Parser for understanding chatbot descriptions.
"""
import nltk
from nltk.tokenize import word_tokenize
import logging

logger = logging.getLogger(__name__)

# Download necessary NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logger.warning(f"Failed to download NLTK data: {e}")

class DescriptionParser:
    """Parse a textual description to understand chatbot requirements."""
    
    def __init__(self):
        self.domain_keywords = {
            'healthcare': ['doctor', 'patient', 'appointment', 'medical', 'health', 'clinic', 'hospital'],
            'customer_service': ['help', 'support', 'service', 'customer', 'issue', 'problem', 'assistance'],
            'food_ordering': ['order', 'food', 'restaurant', 'delivery', 'menu', 'meal', 'dish'],
            'booking': ['book', 'reservation', 'schedule', 'appointment', 'slot', 'availability'],
            'education': ['learn', 'course', 'study', 'student', 'teacher', 'education', 'school', 'university']
        }
        
    def parse(self, description):
        """
        Parse the description to extract domain and features.
        
        Args:
            description (str): Textual description of the chatbot
            
        Returns:
            dict: Parsed information including domain, features, etc.
        """
        logger.info("Parsing chatbot description")
        
        # Tokenize and process
        tokens = word_tokenize(description.lower())
        
        # Detect domain
        domain_scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(token in keywords for token in tokens)
            domain_scores[domain] = score
        
        # Find domain with highest score
        domain = max(domain_scores, key=domain_scores.get)
        
        # Extract features based on domain
        features = self._extract_features(tokens, domain)
        
        parsed_info = {
            'domain': domain,
            'features': features,
            'original_description': description
        }
        
        logger.info(f"Parsed description. Domain: {domain}, Features: {len(features)}")
        return parsed_info
    
    def _extract_features(self, tokens, domain):
        """Extract features based on tokens and detected domain."""
        features = []
        
        # Generic features
        if 'greeting' in tokens or 'hello' in tokens or 'hi' in tokens:
            features.append('greeting')
            
        if 'goodbye' in tokens or 'bye' in tokens:
            features.append('farewell')
            
        # Domain-specific features
        if domain == 'healthcare':
            if 'appointment' in tokens or 'schedule' in tokens or 'book' in tokens:
                features.append('appointment_booking')
            if 'cancel' in tokens:
                features.append('appointment_cancellation')
            if 'doctor' in tokens and ('availability' in tokens or 'available' in tokens):
                features.append('check_doctor_availability')
                
        elif domain == 'customer_service':
            if 'status' in tokens or 'track' in tokens:
                features.append('order_status')
            if 'return' in tokens:
                features.append('process_return')
            if 'complaint' in tokens or 'issue' in tokens or 'problem' in tokens:
                features.append('handle_complaint')
                
        elif domain == 'food_ordering':
            if 'order' in tokens:
                features.append('place_order')
            if 'menu' in tokens:
                features.append('show_menu')
            if 'special' in tokens:
                features.append('show_specials')
                
        return features
