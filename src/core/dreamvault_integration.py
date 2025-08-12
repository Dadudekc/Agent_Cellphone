#!/usr/bin/env python3
"""
DreamVault Integration for Personal Jarvis
Enhances Jarvis with access to ChatGPT threads, product ideas, and workflows from DreamVault
"""
import sqlite3
import json
import logging
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import re

class DreamVaultIntegration:
    """
    Integrates DreamVault database with Jarvis for enhanced capabilities
    """
    
    def __init__(self, dreamvault_path: str = "../DreamVault/data/dreamvault.db"):
        self.dreamvault_path = dreamvault_path
        self.logger = logging.getLogger("DreamVaultIntegration")
        
        # Check if database exists
        if not os.path.exists(dreamvault_path):
            self.logger.warning(f"DreamVault database not found at: {dreamvault_path}")
            self.available = False
        else:
            self.available = True
            self.logger.info(f"DreamVault integration initialized with database: {dreamvault_path}")
    
    def _get_connection(self) -> Optional[sqlite3.Connection]:
        """Get database connection"""
        if not self.available:
            return None
        
        try:
            return sqlite3.connect(self.dreamvault_path)
        except Exception as e:
            self.logger.error(f"Failed to connect to DreamVault database: {e}")
            return None
    
    def get_conversation_summary(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of a specific conversation"""
        conn = self._get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, summary, tags, topics, sentiment, entities, 
                       action_items, decisions, message_count, word_count, created_at
                FROM conversations 
                WHERE id = ?
            """, (conversation_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'summary': row[2],
                    'tags': json.loads(row[3]) if row[3] else [],
                    'topics': json.loads(row[4]) if row[4] else [],
                    'sentiment': json.loads(row[5]) if row[5] else {},
                    'entities': json.loads(row[6]) if row[6] else [],
                    'action_items': json.loads(row[7]) if row[7] else [],
                    'decisions': json.loads(row[8]) if row[8] else [],
                    'message_count': row[9],
                    'word_count': row[10],
                    'created_at': row[11]
                }
            return None
        except Exception as e:
            self.logger.error(f"Error getting conversation summary: {e}")
            return None
        finally:
            conn.close()
    
    def search_conversations(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search conversations using full-text search"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, summary, tags, topics, message_count, created_at
                FROM conversations_fts 
                WHERE conversations_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'summary': row[2],
                    'tags': json.loads(row[3]) if row[3] else [],
                    'topics': json.loads(row[4]) if row[4] else [],
                    'message_count': row[5],
                    'created_at': row[6]
                })
            
            return results
        except Exception as e:
            self.logger.error(f"Error searching conversations: {e}")
            return []
        finally:
            conn.close()
    
    def get_recent_conversations(self, days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute("""
                SELECT id, title, summary, tags, topics, message_count, created_at
                FROM conversations 
                WHERE created_at >= ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (cutoff_date, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'title': row[1],
                    'summary': row[2],
                    'tags': json.loads(row[3]) if row[3] else [],
                    'topics': json.loads(row[4]) if row[4] else [],
                    'message_count': row[5],
                    'created_at': row[6]
                })
            
            return results
        except Exception as e:
            self.logger.error(f"Error getting recent conversations: {e}")
            return []
        finally:
            conn.close()
    
    def get_product_ideas(self, min_value: float = 0.0, limit: int = 10) -> List[Dict[str, Any]]:
        """Get product ideas from IP resurrection data"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT conversation_id, product_ideas, potential_value, tags, summary
                FROM ip_resurrection 
                WHERE potential_value >= ? AND product_ideas != '[]'
                ORDER BY potential_value DESC
                LIMIT ?
            """, (min_value, limit))
            
            results = []
            for row in cursor.fetchall():
                product_ideas = json.loads(row[1]) if row[1] else []
                if product_ideas:  # Only include if there are actual product ideas
                    results.append({
                        'conversation_id': row[0],
                        'product_ideas': product_ideas,
                        'potential_value': row[2],
                        'tags': json.loads(row[3]) if row[3] else [],
                        'summary': row[4]
                    })
            
            return results
        except Exception as e:
            self.logger.error(f"Error getting product ideas: {e}")
            return []
        finally:
            conn.close()
    
    def get_workflows(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get workflows from IP resurrection data"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT conversation_id, workflows, potential_value, tags, summary
                FROM ip_resurrection 
                WHERE workflows != '[]'
                ORDER BY potential_value DESC
                LIMIT ?
            """, (limit,))
            
            results = []
            for row in cursor.fetchall():
                workflows = json.loads(row[1]) if row[1] else []
                if workflows:  # Only include if there are actual workflows
                    results.append({
                        'conversation_id': row[0],
                        'workflows': workflows,
                        'potential_value': row[2],
                        'tags': json.loads(row[3]) if row[3] else [],
                        'summary': row[4]
                    })
            
            return results
        except Exception as e:
            self.logger.error(f"Error getting workflows: {e}")
            return []
        finally:
            conn.close()
    
    def get_abandoned_ideas(self, min_value: float = 0.0, limit: int = 10) -> List[Dict[str, Any]]:
        """Get abandoned ideas that could be resurrected"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT conversation_id, abandoned_ideas, potential_value, tags, summary
                FROM ip_resurrection 
                WHERE potential_value >= ? AND abandoned_ideas != '[]'
                ORDER BY potential_value DESC
                LIMIT ?
            """, (min_value, limit))
            
            results = []
            for row in cursor.fetchall():
                abandoned_ideas = json.loads(row[1]) if row[1] else []
                if abandoned_ideas:  # Only include if there are actual abandoned ideas
                    results.append({
                        'conversation_id': row[0],
                        'abandoned_ideas': abandoned_ideas,
                        'potential_value': row[2],
                        'tags': json.loads(row[3]) if row[3] else [],
                        'summary': row[4]
                    })
            
            return results
        except Exception as e:
            self.logger.error(f"Error getting abandoned ideas: {e}")
            return []
        finally:
            conn.close()
    
    def get_conversation_messages(self, conversation_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get messages from a specific conversation"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role, content, timestamp, message_index
                FROM messages 
                WHERE conversation_id = ?
                ORDER BY message_index
                LIMIT ?
            """, (conversation_id, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'role': row[0],
                    'content': row[1],
                    'timestamp': row[2],
                    'message_index': row[3]
                })
            
            return results
        except Exception as e:
            self.logger.error(f"Error getting conversation messages: {e}")
            return []
        finally:
            conn.close()
    
    def get_topic_insights(self, topic: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get insights about a specific topic across conversations"""
        conn = self._get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, summary, topics, entities, action_items, decisions
                FROM conversations 
                WHERE topics LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (f'%{topic}%', limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'summary': row[1],
                    'topics': json.loads(row[2]) if row[2] else [],
                    'entities': json.loads(row[3]) if row[3] else [],
                    'action_items': json.loads(row[4]) if row[4] else [],
                    'decisions': json.loads(row[5]) if row[5] else []
                })
            
            return results
        except Exception as e:
            self.logger.error(f"Error getting topic insights: {e}")
            return []
        finally:
            conn.close()
    
    def get_high_value_insights(self, min_value: float = 10000.0) -> Dict[str, Any]:
        """Get high-value insights from conversations"""
        conn = self._get_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_conversations,
                    SUM(potential_value) as total_value,
                    AVG(potential_value) as avg_value,
                    COUNT(CASE WHEN product_ideas != '[]' THEN 1 END) as conversations_with_ideas,
                    COUNT(CASE WHEN workflows != '[]' THEN 1 END) as conversations_with_workflows,
                    COUNT(CASE WHEN abandoned_ideas != '[]' THEN 1 END) as conversations_with_abandoned
                FROM ip_resurrection 
                WHERE potential_value >= ?
            """, (min_value,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'total_conversations': row[0],
                    'total_value': row[1],
                    'avg_value': row[2],
                    'conversations_with_ideas': row[3],
                    'conversations_with_workflows': row[4],
                    'conversations_with_abandoned': row[5]
                }
            return {}
        except Exception as e:
            self.logger.error(f"Error getting high value insights: {e}")
            return {}
        finally:
            conn.close()
    
    def suggest_actions_based_on_history(self, current_context: str) -> List[Dict[str, Any]]:
        """Suggest actions based on similar historical conversations"""
        # Search for similar conversations
        similar_conversations = self.search_conversations(current_context, limit=5)
        
        suggestions = []
        for conv in similar_conversations:
            # Extract action items from similar conversations
            action_items = conv.get('action_items', [])
            for action in action_items:
                if isinstance(action, dict) and 'action' in action:
                    suggestions.append({
                        'action': action['action'],
                        'priority': action.get('priority', 'medium'),
                        'source_conversation': conv['id'],
                        'confidence': action.get('confidence', 0.5)
                    })
        
        return suggestions
    
    def get_learning_recommendations(self) -> Dict[str, Any]:
        """Get learning recommendations based on conversation patterns"""
        conn = self._get_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            
            # Get most common topics
            cursor.execute("""
                SELECT topics, COUNT(*) as count
                FROM conversations 
                WHERE topics IS NOT NULL AND topics != '[]'
                GROUP BY topics
                ORDER BY count DESC
                LIMIT 5
            """)
            
            topic_patterns = []
            for row in cursor.fetchall():
                topics = json.loads(row[0]) if row[0] else []
                topic_patterns.append({
                    'topics': topics,
                    'frequency': row[1]
                })
            
            # Get most valuable insights
            cursor.execute("""
                SELECT c.summary, ir.potential_value, ir.tags
                FROM ip_resurrection ir
                JOIN conversations c ON ir.conversation_id = c.id
                WHERE ir.potential_value > 5000
                ORDER BY ir.potential_value DESC
                LIMIT 3
            """)
            
            valuable_insights = []
            for row in cursor.fetchall():
                valuable_insights.append({
                    'summary': row[0],
                    'value': row[1],
                    'tags': json.loads(row[2]) if row[2] else []
                })
            
            return {
                'topic_patterns': topic_patterns,
                'valuable_insights': valuable_insights
            }
        except Exception as e:
            self.logger.error(f"Error getting learning recommendations: {e}")
            return {}
        finally:
            conn.close()

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Test DreamVault integration
    dv = DreamVaultIntegration()
    
    if dv.available:
        print("DreamVault Integration Test")
        print("=" * 40)
        
        # Test recent conversations
        recent = dv.get_recent_conversations(days=7, limit=3)
        print(f"Recent conversations: {len(recent)}")
        
        # Test product ideas
        ideas = dv.get_product_ideas(min_value=5000, limit=3)
        print(f"Product ideas: {len(ideas)}")
        
        # Test high value insights
        insights = dv.get_high_value_insights(min_value=10000)
        print(f"High value insights: {insights}")
        
        # Test learning recommendations
        recommendations = dv.get_learning_recommendations()
        print(f"Learning recommendations: {len(recommendations.get('topic_patterns', []))} topic patterns")
    else:
        print("DreamVault database not available") 