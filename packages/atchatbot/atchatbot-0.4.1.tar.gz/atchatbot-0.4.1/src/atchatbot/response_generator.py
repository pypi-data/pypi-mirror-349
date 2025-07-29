# src/atchatbot/response_generator.py
"""
Response generation for the chatbot.
"""
import random
import logging

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generate responses for the chatbot."""
    
    def __init__(self, domain, features):
        """
        Initialize the response generator.
        
        Args:
            domain (str): The domain of the chatbot
            features (list): List of features the chatbot supports
        """
        self.domain = domain
        self.features = features
        self.responses = self._generate_responses()
        
        logger.info(f"Initialized response generator for domain: {domain}")
        
    def _generate_responses(self):
        """Generate response templates based on domain and features."""
        responses = {}
        
        # Add generic responses
        responses['greeting'] = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Greetings! How may I assist you?"
        ]
        
        responses['farewell'] = [
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Bye! Feel free to come back if you need anything else."
        ]
        
        responses['help'] = [
            f"I'm a {self.domain} chatbot. I can help you with: {', '.join(self.features)}.",
            f"I'm here to assist with {self.domain} related queries. Just tell me what you need!",
            f"I can help with {self.domain} tasks. What would you like to do?"
        ]
        
        responses['unknown'] = [
            "I'm sorry, I didn't understand that. Could you rephrase?",
            "I'm not sure what you mean. Can you explain differently?",
            "I didn't catch that. What can I help you with?"
        ]
        
        # Domain-specific responses
        if self.domain == 'healthcare':
            if 'appointment_booking' in self.features:
                responses['book_appointment'] = [
                    "I'd be happy to help you book an appointment. What day works for you?",
                    "Let's schedule your appointment. Do you have a preferred doctor?",
                    "Sure, I can book an appointment for you. What time would you prefer?"
                ]
                
            if 'appointment_cancellation' in self.features:
                responses['cancel_appointment'] = [
                    "I can help cancel your appointment. Could you provide your appointment details?",
                    "Sorry to hear you need to cancel. Can you tell me when your appointment was scheduled?",
                    "I'll assist you with cancelling. Do you have your appointment ID?"
                ]
                
        elif self.domain == 'customer_service':
            if 'order_status' in self.features:
                responses['check_order'] = [
                    "I'd be happy to check your order status. Could you provide your order number?",
                    "Let me look up that order for you. What's your order ID?",
                    "I can track your order. Please share your order reference number."
                ]
                
            if 'handle_complaint' in self.features:
                responses['complaint'] = [
                    "I'm sorry to hear you're having an issue. Could you describe the problem?",
                    "I apologize for the inconvenience. What seems to be the problem?",
                    "Let me help address your complaint. Can you provide more details?"
                ]
                
        elif self.domain == 'food_ordering':
            if 'place_order' in self.features:
                responses['order_food'] = [
                    "I'd be happy to take your order. What would you like to eat?",
                    "Ready to order? What can I get for you today?",
                    "Let's place your food order. What would you like to order?"
                ]
                
            if 'show_menu' in self.features:
                responses['view_menu'] = [
                    "Here's our menu: [Menu would be displayed here]",
                    "Let me show you what we have available today: [Menu items]",
                    "Our current menu offers: [List of dishes]"
                ]
                
        logger.info(f"Generated responses for {len(responses)} intents")
        return responses
        
    def generate_response(self, intent):
        """
        Generate a response based on the detected intent.
        
        Args:
            intent (str): The detected intent
            
        Returns:
            str: A response message
        """
        if intent in self.responses:
            return random.choice(self.responses[intent])
        
        return random.choice(self.responses['unknown'])
