#!/usr/bin/env python3
"""
Memory System for Personal Jarvis
Enables Jarvis to remember conversations, user preferences, and context
"""

import json
import time
import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import sqlite3
import threading

class MemorySystem:
    """
    Memory system for Personal Jarvis to remember conversations and context
    """
    
    def __init__(self, memory_file: str = "jarvis_memory.json", db_file: str = "jarvis_memory.db"):
        self.memory_file = memory_file
        self.db_file = db_file
        self.logger = logging.getLogger("MemorySystem")
        
        # In-memory cache
        self.short_term_memory = []
        self.user_preferences = {}
        self.conversation_context = {}
        
        # Initialize database
        self._init_database()
        
        # Load existing memory
        self._load_memory()
        
        self.logger.info("Memory system initialized")
    
    def _init_database(self):
        """Initialize SQLite database for persistent memory"""
        try:
            self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            # Create tables
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    user_message TEXT,
                    jarvis_response TEXT,
                    context TEXT,
                    session_id TEXT
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp REAL
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_info (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    timestamp REAL
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS learned_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern TEXT,
                    action TEXT,
                    success_rate REAL,
                    last_used REAL,
                    usage_count INTEGER DEFAULT 0
                )
            ''')
            
            self.conn.commit()
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
    
    def _load_memory(self):
        """Load existing memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_preferences = data.get('user_preferences', {})
                    self.conversation_context = data.get('conversation_context', {})
                    self.logger.info("Memory loaded from file")
        except Exception as e:
            self.logger.error(f"Failed to load memory: {e}")
    
    def _save_memory(self):
        """Save memory to file"""
        try:
            data = {
                'user_preferences': self.user_preferences,
                'conversation_context': self.conversation_context,
                'last_updated': time.time()
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save memory: {e}")
    
    def remember_conversation(self, user_message: str, jarvis_response: str, context: str = "", session_id: str = ""):
        """Remember a conversation exchange"""
        try:
            # Add to short-term memory
            conversation = {
                'timestamp': time.time(),
                'user_message': user_message,
                'jarvis_response': jarvis_response,
                'context': context,
                'session_id': session_id
            }
            self.short_term_memory.append(conversation)
            
            # Keep only last 50 conversations in short-term memory
            if len(self.short_term_memory) > 50:
                self.short_term_memory = self.short_term_memory[-50:]
            
            # Store in database
            self.cursor.execute('''
                INSERT INTO conversations (timestamp, user_message, jarvis_response, context, session_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (time.time(), user_message, jarvis_response, context, session_id))
            self.conn.commit()
            
            self.logger.info(f"Conversation remembered: {user_message[:50]}...")
            
        except Exception as e:
            self.logger.error(f"Failed to remember conversation: {e}")
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations"""
        try:
            self.cursor.execute('''
                SELECT timestamp, user_message, jarvis_response, context, session_id
                FROM conversations
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            conversations = []
            for row in self.cursor.fetchall():
                conversations.append({
                    'timestamp': row[0],
                    'user_message': row[1],
                    'jarvis_response': row[2],
                    'context': row[3],
                    'session_id': row[4]
                })
            
            return conversations
            
        except Exception as e:
            self.logger.error(f"Failed to get recent conversations: {e}")
            return []
    
    def get_conversation_context(self, session_id: str = "") -> Dict:
        """Get conversation context for current session"""
        try:
            if session_id:
                self.cursor.execute('''
                    SELECT user_message, jarvis_response, context
                    FROM conversations
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 5
                ''', (session_id,))
            else:
                self.cursor.execute('''
                    SELECT user_message, jarvis_response, context
                    FROM conversations
                    ORDER BY timestamp DESC
                    LIMIT 5
                ''')
            
            context = {
                'recent_messages': [],
                'current_topic': '',
                'user_preferences': self.user_preferences.copy()
            }
            
            for row in self.cursor.fetchall():
                context['recent_messages'].append({
                    'user': row[0],
                    'jarvis': row[1],
                    'context': row[2]
                })
            
            return context
            
        except Exception as e:
            self.logger.error(f"Failed to get conversation context: {e}")
            return {'recent_messages': [], 'current_topic': '', 'user_preferences': {}}
    
    def learn_user_preference(self, key: str, value: Any):
        """Learn a user preference"""
        try:
            self.user_preferences[key] = value
            
            # Store in database
            self.cursor.execute('''
                INSERT OR REPLACE INTO user_preferences (key, value, timestamp)
                VALUES (?, ?, ?)
            ''', (key, json.dumps(value), time.time()))
            self.conn.commit()
            
            self._save_memory()
            self.logger.info(f"Learned user preference: {key} = {value}")
            
        except Exception as e:
            self.logger.error(f"Failed to learn user preference: {e}")
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        return self.user_preferences.get(key, default)
    
    def learn_user_info(self, key: str, value: str):
        """Learn information about the user"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO user_info (key, value, timestamp)
                VALUES (?, ?, ?)
            ''', (key, value, time.time()))
            self.conn.commit()
            
            self.logger.info(f"Learned user info: {key} = {value}")
            
        except Exception as e:
            self.logger.error(f"Failed to learn user info: {e}")
    
    def get_user_info(self, key: str) -> Optional[str]:
        """Get information about the user"""
        try:
            self.cursor.execute('SELECT value FROM user_info WHERE key = ?', (key,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            self.logger.error(f"Failed to get user info: {e}")
            return None
    
    def learn_command(self, pattern: str, action: str, success: bool = True):
        """Learn a command pattern and its success rate"""
        try:
            # Get existing command
            self.cursor.execute('SELECT success_rate, usage_count FROM learned_commands WHERE pattern = ?', (pattern,))
            result = self.cursor.fetchone()
            
            if result:
                current_success_rate = result[0]
                usage_count = result[1] + 1
                
                # Update success rate
                if success:
                    new_success_rate = (current_success_rate * (usage_count - 1) + 1) / usage_count
                else:
                    new_success_rate = (current_success_rate * (usage_count - 1)) / usage_count
                
                self.cursor.execute('''
                    UPDATE learned_commands 
                    SET success_rate = ?, usage_count = ?, last_used = ?
                    WHERE pattern = ?
                ''', (new_success_rate, usage_count, time.time(), pattern))
            else:
                success_rate = 1.0 if success else 0.0
                self.cursor.execute('''
                    INSERT INTO learned_commands (pattern, action, success_rate, last_used, usage_count)
                    VALUES (?, ?, ?, ?, 1)
                ''', (pattern, action, success_rate, time.time()))
            
            self.conn.commit()
            
        except Exception as e:
            self.logger.error(f"Failed to learn command: {e}")
    
    def get_best_commands(self, limit: int = 10) -> List[Dict]:
        """Get the most successful commands"""
        try:
            self.cursor.execute('''
                SELECT pattern, action, success_rate, usage_count
                FROM learned_commands
                WHERE success_rate > 0.5
                ORDER BY success_rate DESC, usage_count DESC
                LIMIT ?
            ''', (limit,))
            
            commands = []
            for row in self.cursor.fetchall():
                commands.append({
                    'pattern': row[0],
                    'action': row[1],
                    'success_rate': row[2],
                    'usage_count': row[3]
                })
            
            return commands
            
        except Exception as e:
            self.logger.error(f"Failed to get best commands: {e}")
            return []
    
    def search_memory(self, query: str, limit: int = 10) -> List[Dict]:
        """Search through memory for relevant information"""
        try:
            self.cursor.execute('''
                SELECT timestamp, user_message, jarvis_response, context
                FROM conversations
                WHERE user_message LIKE ? OR jarvis_response LIKE ? OR context LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit))
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'timestamp': row[0],
                    'user_message': row[1],
                    'jarvis_response': row[2],
                    'context': row[3]
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to search memory: {e}")
            return []
    
    def get_memory_summary(self) -> Dict:
        """Get a summary of memory contents"""
        try:
            # Count conversations
            self.cursor.execute('SELECT COUNT(*) FROM conversations')
            conversation_count = self.cursor.fetchone()[0]
            
            # Count user preferences
            self.cursor.execute('SELECT COUNT(*) FROM user_preferences')
            preference_count = self.cursor.fetchone()[0]
            
            # Count user info
            self.cursor.execute('SELECT COUNT(*) FROM user_info')
            info_count = self.cursor.fetchone()[0]
            
            # Count learned commands
            self.cursor.execute('SELECT COUNT(*) FROM learned_commands')
            command_count = self.cursor.fetchone()[0]
            
            # Get oldest and newest conversations
            self.cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM conversations')
            time_range = self.cursor.fetchone()
            
            return {
                'conversation_count': conversation_count,
                'preference_count': preference_count,
                'info_count': info_count,
                'command_count': command_count,
                'oldest_conversation': time_range[0] if time_range[0] else None,
                'newest_conversation': time_range[1] if time_range[1] else None,
                'short_term_memory_size': len(self.short_term_memory)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get memory summary: {e}")
            return {}
    
    def clear_old_memory(self, days: int = 30):
        """Clear old memory entries"""
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            
            self.cursor.execute('DELETE FROM conversations WHERE timestamp < ?', (cutoff_time,))
            deleted_count = self.cursor.rowcount
            self.conn.commit()
            
            self.logger.info(f"Cleared {deleted_count} old conversation entries")
            
        except Exception as e:
            self.logger.error(f"Failed to clear old memory: {e}")
    
    def close(self):
        """Close the memory system"""
        try:
            self._save_memory()
            self.conn.close()
            self.logger.info("Memory system closed")
        except Exception as e:
            self.logger.error(f"Error closing memory system: {e}")

# Example usage
if __name__ == "__main__":
    memory = MemorySystem()
    
    # Test memory system
    memory.remember_conversation("Hello Jarvis", "Hello! How can I help you today?", "greeting")
    memory.learn_user_preference("voice_speed", 150)
    memory.learn_user_info("name", "User")
    
    print("Memory system test completed!")
    print(memory.get_memory_summary())
    
    memory.close() 