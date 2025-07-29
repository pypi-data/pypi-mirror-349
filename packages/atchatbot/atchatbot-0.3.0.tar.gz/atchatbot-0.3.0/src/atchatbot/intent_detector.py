# src/atchatbot/intent_detector.py
"""
Intent detection for the chatbot.
"""
import re
import logging
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

class IntentDetector:
    """Detect intents from user inputs."""
    
    def __init__(self, domain, features):
        """
        Initialize the intent detector.
        
        Args:
            domain (str): The domain of the chatbot
            features (list): List of features the chatbot supports
        """
        self.domain = domain
        self.features = features
        self.intents = self._generate_intents()
        
        logger.info(f"Initialized intent detector for domain: {domain}")
        
    def _generate_intents(self):
        """Generate intent patterns based on domain and features."""
        intents = {}
        
        # Add generic intents
        intents['greeting'] = {
            'patterns': [
                r'hello', r'hi', r'hey', r'good morning', r'good afternoon', 
                r'good evening', r'howdy', r'greetings'
            ]
        }
        
        intents['farewell'] = {
            'patterns': [
                r'bye', r'goodbye', r'see you', r'talk to you later', 
                r'have a good day', r'until next time'
            ]
        }
        
        intents['help'] = {
            'patterns': [
                r'help', r'assist', r'support', r'what can you do', 
                r'how does this work', r'guide me'
            ]
        }
        
        # Domain-specific intents
        if self.domain == 'healthcare':
            if 'appointment_booking' in self.features:
                intents['book_appointment'] = {
                    'patterns': [
                        r'book (an )?appointment', r'schedule (a )?visit', 
                        r'make (an )?appointment', r'see (a )?doctor', 
                        r'set up (an )?appointment'
                    ]
                }
                
            if 'appointment_cancellation' in self.features:
                intents['cancel_appointment'] = {
                    'patterns': [
                        r'cancel (my )?appointment', r'remove (my )?booking', 
                        r'delete (my )?appointment', r'cancel (my )?visit'
                    ]
                }
                
        elif self.domain == 'customer_service':
            if 'order_status' in self.features:
                intents['check_order'] = {
                    'patterns': [
                        r'check (my )?order', r'order status', 
                        r'where is my order', r'track (my )?package',
                        r'track (my )?order'
                    ]
                }
                
            if 'handle_complaint' in self.features:
                intents['complaint'] = {
                    'patterns': [
                        r'(file|make|have|submit) (a )?complaint', 
                        r'problem with', r'issue with', r'not working', r'broken'
                    ]
                }
                
        elif self.domain == 'food_ordering':
            if 'place_order' in self.features:
                intents['order_food'] = {
                    'patterns': [
                        r'order food', r'place (an )?order', r'get (some )?food', 
                        r'order (a )?meal', r'order (a )?dish'
                    ]
                }
                
            if 'show_menu' in self.features:
                intents['view_menu'] = {
                    'patterns': [
                        r'menu', r'what food do you have', r'what can i order', 
                        r'dishes available', r'show me (the )?menu'
                    ]
                }
                
        logger.info(f"Generated {len(intents)} intents")
        return intents
        
    def detect_intent(self, user_input):
        """
        Detect the intent of a user input.
        
        Args:
            user_input (str): The user's message
            
        Returns:
            tuple: (intent_name, confidence_score)
        """
        user_input = user_input.lower()
        scores = defaultdict(float)
        
        # Check each intent
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data['patterns']:
                if re.search(pattern, user_input, re.IGNORECASE):
                    scores[intent_name] += 1
        
        # Find the intent with the highest score
        if scores:
            best_intent = max(scores, key=scores.get)
            confidence = scores[best_intent] / len(self.intents[best_intent]['patterns'])
            return best_intent, confidence
        
        # Default fallback
        return 'unknown', 0.0
