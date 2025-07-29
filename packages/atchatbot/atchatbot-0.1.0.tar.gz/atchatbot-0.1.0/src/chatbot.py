# src/atchatbot/chatbot.py
"""
Main Chatbot class for the ATChatbot library.
"""
import logging
from .intent_detector import IntentDetector
from .response_generator import ResponseGenerator

logger = logging.getLogger(__name__)

class Chatbot:
    """A chatbot that can understand user inputs and generate responses."""
    
    def __init__(self, name, domain, features, description=""):
        """
        Initialize the chatbot.
        
        Args:
            name (str): The name of the chatbot
            domain (str): The domain the chatbot operates in
            features (list): List of features the chatbot supports
            description (str): Original description of the chatbot
        """
        self.name = name
        self.domain = domain
        self.features = features
        self.description = description
        self.intent_detector = IntentDetector(domain, features)
        self.response_generator = ResponseGenerator(domain, features)
        self.conversation_history = []
        
        logger.info(f"Initialized {name} chatbot for domain: {domain}")
        
    def process_message(self, message):
        """
        Process a user message and generate a response.
        
        Args:
            message (str): The user's message
            
        Returns:
            str: The chatbot's response
        """
        # Log the incoming message
        logger.info(f"Received message: {message}")
        
        # Detect intent
        intent, confidence = self.intent_detector.detect_intent(message)
        logger.info(f"Detected intent: {intent} with confidence: {confidence:.2f}")
        
        # Generate response
        response = self.response_generator.generate_response(intent)
        
        # Store in conversation history
        self.conversation_history.append({
            'user': message,
            'bot': response,
            'intent': intent,
            'confidence': confidence
        })
        
        return response
    
    def run_interactive(self):
        """Run the chatbot in interactive mode."""
        print(f"\n{self.name} is now running. Type 'exit' to quit.\n")
        
        # Starting message
        print(f"{self.name}: Hello! How can I help you today?")
        
        while True:
            # Get user input
            user_input = input("You: ")
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"{self.name}: Goodbye! Have a great day!")
                break
                
            # Process and respond
            response = self.process_message(user_input)
            print(f"{self.name}: {response}")
