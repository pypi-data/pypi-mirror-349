# src/atchatbot/__init__.py
"""
ATChatbot - A universal chatbot generation library.
"""

__version__ = '0.1.0'

from .core import generate_chatbot
from .chatbot import Chatbot

__all__ = ['generate_chatbot', 'Chatbot']
