# src/atchatbot/core.py
"""
Core functionality for the ATChatbot library.
"""
import logging
from .parser import DescriptionParser
from .chatbot import Chatbot
from .utils import ensure_dir
import os

logger = logging.getLogger(__name__)

def generate_chatbot(description, name="ATBot"):
    """
    Generate a chatbot from a textual description.
    
    Args:
        description (str): A textual description of the chatbot
        name (str, optional): The name of the chatbot. Defaults to "ATBot".
        
    Returns:
        Chatbot: An instance of the generated chatbot
    """
    logger.info(f"Generating chatbot from description: {description}")
    
    # Parse the description
    parser = DescriptionParser()
    parsed_info = parser.parse(description)
    
    # Extract information
    domain = parsed_info['domain']
    features = parsed_info['features']
    
    # Generate the chatbot
    chatbot = Chatbot(
        name=name,
        domain=domain,
        features=features,
        description=description
    )
    
    logger.info(f"Generated chatbot: {name} for domain: {domain}")
    return chatbot
