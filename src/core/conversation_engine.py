#!/usr/bin/env python3
"""
Conversation Engine for Personal Jarvis
Enables intelligent, contextual conversations with memory and learning
"""

import time
import logging
import re
import random
from typing import Dict, List, Optional, Tuple
from memory_system import MemorySystem

class ConversationEngine:
    """
    AI-powered conversation engine for Personal Jarvis
    """
    
    def __init__(self, memory_system: MemorySystem):
        self.memory = memory_system
        self.logger = logging.getLogger("ConversationEngine")
        self.session_id = f"session_{int(time.time())}"
        
        # Conversation patterns and responses
        self.conversation_patterns = {
            'greetings': {
                'patterns': [
                    r'hello|hi|hey|greetings|good morning|good afternoon|good evening',
                    r'how are you|how do you do|what\'s up',
                    r'are you there|jarvis|wake up'
                ],
                'responses': [
                    "Hello! I'm here and ready to help you.",
                    "Hi there! How can I assist you today?",
                    "Greetings! I'm listening and ready to work.",
                    "Hello! What would you like me to help you with?"
                ]
            },
            'identity': {
                'patterns': [
                    r'who are you|what are you|tell me about yourself',
                    r'what can you do|what are your capabilities',
                    r'are you ai|are you artificial intelligence'
                ],
                'responses': [
                    "I'm Jarvis, your personal AI assistant. I can help you control your computer, manage development tasks, and have conversations with you.",
                    "I'm your AI assistant Jarvis. I can see your screen, hear your voice, control applications, and learn from our interactions.",
                    "I'm Jarvis, an AI assistant designed to help you with development and computer tasks. I have vision, hearing, and can control your system."
                ]
            },
            'memory': {
                'patterns': [
                    r'do you remember|can you remember|what do you know about me',
                    r'what have we talked about|our previous conversations',
                    r'do you know who i am|what\'s my name'
                ],
                'responses': [
                    "Let me check my memory...",
                    "I'll look through our conversation history...",
                    "Let me recall what we've discussed..."
                ]
            },
            'learning': {
                'patterns': [
                    r'learn|remember|save|store|memorize',
                    r'my name is|i am|call me',
                    r'i like|i prefer|my favorite'
                ],
                'responses': [
                    "I'll remember that for you.",
                    "Got it! I've stored that information.",
                    "I've learned that about you."
                ]
            },
            'gratitude': {
                'patterns': [
                    r'thank you|thanks|appreciate it|good job',
                    r'well done|excellent|perfect|great'
                ],
                'responses': [
                    "You're welcome! I'm happy to help.",
                    "My pleasure! Is there anything else you need?",
                    "Thank you! I enjoy working with you."
                ]
            },
            'farewell': {
                'patterns': [
                    r'goodbye|bye|see you|later|exit|quit',
                    r'stop|end|shut down|turn off'
                ],
                'responses': [
                    "Goodbye! I'll be here when you need me.",
                    "See you later! Don't hesitate to call if you need help.",
                    "Farewell! I'm always ready to assist you."
                ]
            },
            'confusion': {
                'patterns': [
                    r'i don\'t understand|what do you mean|confused',
                    r'that doesn\'t make sense|i\'m lost'
                ],
                'responses': [
                    "I apologize for the confusion. Let me try to clarify...",
                    "I understand that wasn't clear. Let me explain differently...",
                    "I see the confusion. Let me break this down..."
                ]
            },
            'help': {
                'patterns': [
                    r'help|what can you do|show me|guide me',
                    r'how do i|how can i|instructions'
                ],
                'responses': [
                    "I can help you with many tasks. Here are some examples:",
                    "Let me show you what I'm capable of:",
                    "I'm here to assist you with various tasks. Here's what I can do:"
                ]
            }
        }
        
        # Context tracking
        self.current_topic = ""
        self.conversation_context = {}
        self.session_id = f"session_{int(time.time())}"
        
        self.logger.info("Conversation engine initialized")
    
    def generate_response(self, user_message: str, context: Dict = None) -> str:
        """
        Generate an intelligent response to user input
        """
        try:
            # Normalize input
            user_message_lower = user_message.lower().strip()
            
            # Get conversation context
            if context is None:
                context = self.memory.get_conversation_context(self.session_id)
            
            # Check for specific patterns first
            response = self._check_specific_patterns(user_message_lower, context)
            if response:
                return response
            
            # Check for learning opportunities
            if self._is_learning_request(user_message_lower):
                return self._handle_learning(user_message_lower)
            
            # Check for memory queries
            if self._is_memory_query(user_message_lower):
                return self._handle_memory_query(user_message_lower, context)
            
            # Check for help requests
            if self._is_help_request(user_message_lower):
                return self._handle_help_request(user_message_lower)
            
            # Check for identity questions
            if self._is_identity_question(user_message_lower):
                return self._handle_identity_question(user_message_lower)
            
            # Check for greetings
            if self._is_greeting(user_message_lower):
                return self._handle_greeting(user_message_lower, context)
            
            # Check for farewells
            if self._is_farewell(user_message_lower):
                return self._handle_farewell(user_message_lower)
            
            # Check for gratitude
            if self._is_gratitude(user_message_lower):
                return self._handle_gratitude(user_message_lower)
            
            # Default response for unrecognized input
            return self._generate_default_response(user_message_lower, context)
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing that right now. Could you rephrase?"
    
    def _check_specific_patterns(self, message: str, context: Dict) -> Optional[str]:
        """Check for specific conversation patterns"""
        
        # Check for name learning
        name_match = re.search(r'my name is (.+)', message)
        if name_match:
            name = name_match.group(1).strip()
            self.memory.learn_user_info("name", name)
            return f"Nice to meet you, {name}! I'll remember your name."
        
        # Check for preference learning
        preference_match = re.search(r'i (like|prefer|love) (.+)', message)
        if preference_match:
            preference = preference_match.group(2).strip()
            self.memory.learn_user_preference("likes", preference)
            return f"I'll remember that you like {preference}."
        
        # Check for command learning
        if "remember this command" in message or "learn this" in message:
            # Extract the command pattern
            command_match = re.search(r'when i say (.+), you should (.+)', message)
            if command_match:
                pattern = command_match.group(1).strip()
                action = command_match.group(2).strip()
                self.memory.learn_command(pattern, action)
                return f"I've learned that when you say '{pattern}', I should {action}."
        
        return None
    
    def _is_learning_request(self, message: str) -> bool:
        """Check if user wants to teach Jarvis something"""
        learning_patterns = [
            r'learn|remember|save|store|memorize',
            r'teach you|show you|tell you',
            r'my name is|i am|call me'
        ]
        return any(re.search(pattern, message) for pattern in learning_patterns)
    
    def _handle_learning(self, message: str) -> str:
        """Handle learning requests"""
        if "my name is" in message:
            name_match = re.search(r'my name is (.+)', message)
            if name_match:
                name = name_match.group(1).strip()
                self.memory.learn_user_info("name", name)
                return f"Thank you! I'll remember your name is {name}."
        
        if "i like" in message or "i prefer" in message:
            like_match = re.search(r'i (like|prefer|love) (.+)', message)
            if like_match:
                preference = like_match.group(2).strip()
                self.memory.learn_user_preference("likes", preference)
                return f"I've learned that you like {preference}. I'll remember that!"
        
        return "I'm ready to learn! What would you like me to remember?"
    
    def _is_memory_query(self, message: str) -> bool:
        """Check if user is asking about memory"""
        memory_patterns = [
            r'do you remember|can you remember',
            r'what do you know about me',
            r'what have we talked about',
            r'do you know who i am'
        ]
        return any(re.search(pattern, message) for pattern in memory_patterns)
    
    def _handle_memory_query(self, message: str, context: Dict) -> str:
        """Handle memory queries"""
        # Get user info
        user_name = self.memory.get_user_info("name")
        user_preferences = self.memory.get_user_preference("likes")
        
        response_parts = []
        
        if user_name:
            response_parts.append(f"I know your name is {user_name}.")
        
        if user_preferences:
            response_parts.append(f"I remember you like {user_preferences}.")
        
        # Get recent conversations
        recent_conversations = self.memory.get_recent_conversations(3)
        if recent_conversations:
            response_parts.append("We've had several conversations recently.")
        
        if response_parts:
            return " ".join(response_parts)
        else:
            return "I'm still getting to know you. Feel free to tell me more about yourself!"
    
    def _is_help_request(self, message: str) -> bool:
        """Check if user is asking for help"""
        help_patterns = [
            r'help|what can you do|show me|guide me',
            r'how do i|how can i|instructions'
        ]
        return any(re.search(pattern, message) for pattern in help_patterns)
    
    def _handle_help_request(self, message: str) -> str:
        """Handle help requests"""
        help_text = """
        I can help you with many tasks:
        
        🖥️ Computer Control:
        - Open and close applications
        - Control Cursor editor
        - Navigate files and folders
        
        💻 Development Tasks:
        - Run tests and build projects
        - Install dependencies
        - Check for errors and fix bugs
        - Commit and push code changes
        
        👁️ Vision and Analysis:
        - See what's on your screen
        - Analyze screen content
        - Find and click on text
        
        🎤 Voice Interaction:
        - Respond to voice commands
        - Have natural conversations
        - Learn your preferences
        
        🧠 Memory and Learning:
        - Remember our conversations
        - Learn your preferences
        - Adapt to your workflow
        
        Just tell me what you'd like me to do!
        """
        
        return "I'm here to help! " + help_text
    
    def _is_identity_question(self, message: str) -> bool:
        """Check if user is asking about Jarvis's identity"""
        identity_patterns = [
            r'who are you|what are you',
            r'are you ai|are you artificial intelligence',
            r'tell me about yourself'
        ]
        return any(re.search(pattern, message) for pattern in identity_patterns)
    
    def _handle_identity_question(self, message: str) -> str:
        """Handle identity questions"""
        responses = [
            "I'm Jarvis, your personal AI assistant. I'm designed to help you with development tasks, computer control, and have meaningful conversations.",
            "I'm an AI assistant named Jarvis. I can see your screen, hear your voice, control applications, and learn from our interactions to better serve you.",
            "I'm Jarvis, your AI companion. I combine vision, hearing, and intelligence to help you with coding, system control, and daily tasks."
        ]
        return random.choice(responses)
    
    def _is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        greeting_patterns = [
            r'hello|hi|hey|greetings',
            r'good morning|good afternoon|good evening',
            r'how are you|what\'s up'
        ]
        return any(re.search(pattern, message) for pattern in greeting_patterns)
    
    def _handle_greeting(self, message: str, context: Dict) -> str:
        """Handle greetings"""
        user_name = self.memory.get_user_info("name")
        
        if user_name:
            responses = [
                f"Hello {user_name}! Great to see you again.",
                f"Hi {user_name}! How can I help you today?",
                f"Greetings {user_name}! What would you like to work on?"
            ]
        else:
            responses = [
                "Hello! I'm Jarvis, your AI assistant. How can I help you today?",
                "Hi there! I'm here to assist you with your tasks.",
                "Greetings! I'm ready to help you with development and computer tasks."
            ]
        
        return random.choice(responses)
    
    def _is_farewell(self, message: str) -> bool:
        """Check if message is a farewell"""
        farewell_patterns = [
            r'goodbye|bye|see you|later',
            r'exit|quit|stop|end'
        ]
        return any(re.search(pattern, message) for pattern in farewell_patterns)
    
    def _handle_farewell(self, message: str) -> str:
        """Handle farewells"""
        responses = [
            "Goodbye! I'll be here when you need me.",
            "See you later! Don't hesitate to call if you need help.",
            "Farewell! I'm always ready to assist you.",
            "Take care! I'm here whenever you need assistance."
        ]
        return random.choice(responses)
    
    def _is_gratitude(self, message: str) -> bool:
        """Check if message expresses gratitude"""
        gratitude_patterns = [
            r'thank you|thanks|appreciate it',
            r'good job|well done|excellent'
        ]
        return any(re.search(pattern, message) for pattern in gratitude_patterns)
    
    def _handle_gratitude(self, message: str) -> str:
        """Handle gratitude"""
        responses = [
            "You're welcome! I'm happy to help.",
            "My pleasure! Is there anything else you need?",
            "Thank you! I enjoy working with you.",
            "Glad I could help! What's next?"
        ]
        return random.choice(responses)
    
    def _generate_default_response(self, message: str, context: Dict) -> str:
        """Generate a default response for unrecognized input"""
        
        # Check if this might be a command
        if any(word in message for word in ['open', 'close', 'run', 'start', 'stop', 'find', 'search']):
            return "I understand you might want me to perform an action. Could you be more specific about what you'd like me to do?"
        
        # Check if this is a question
        if message.endswith('?') or any(word in message for word in ['what', 'how', 'why', 'when', 'where']):
            return "That's an interesting question. Let me think about how I can best help you with that."
        
        # Generic response
        responses = [
            "I hear you. Could you tell me more about what you'd like me to help you with?",
            "I understand. How can I assist you with that?",
            "I see. What would you like me to do about that?",
            "I'm listening. What's your next step?"
        ]
        
        return random.choice(responses)
    
    def remember_conversation(self, user_message: str, jarvis_response: str, context: str = ""):
        """Remember a conversation exchange"""
        self.memory.remember_conversation(user_message, jarvis_response, context, self.session_id)
    
    def get_conversation_summary(self) -> Dict:
        """Get a summary of the current conversation session"""
        return {
            'session_id': self.session_id,
            'memory_summary': self.memory.get_memory_summary()
        }

# Example usage
if __name__ == "__main__":
    from memory_system import MemorySystem
    
    # Test conversation engine
    memory = MemorySystem()
    engine = ConversationEngine(memory)
    
    # Test conversations
    test_messages = [
        "Hello Jarvis",
        "My name is John",
        "I like Python programming",
        "Do you remember my name?",
        "What can you do?",
        "Thank you for your help",
        "Goodbye"
    ]
    
    for message in test_messages:
        response = engine.generate_response(message)
        print(f"User: {message}")
        print(f"Jarvis: {response}")
        print()
        engine.remember_conversation(message, response)
    
    memory.close() 