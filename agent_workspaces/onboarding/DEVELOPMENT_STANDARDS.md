# 💻 Dream.OS Development Standards

## 📋 Overview
Development standards and guidelines for agents in the Dream.OS multi-agent system.

## 🏗️ Code Structure

### File Organization
- **Use descriptive filenames** that indicate purpose
- **Group related files** in appropriate directories
- **Separate concerns** - one file per major functionality
- **Use consistent naming** conventions across the project
- **Document file purposes** in header comments

### Code Organization
```python
# File header with purpose and author
#!/usr/bin/env python3
"""
Purpose: Brief description of what this file does
Author: Agent responsible for this code
Date: Creation/modification date
"""

# Imports organized by standard library, third-party, local
import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional

# Constants at the top
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Classes and functions with clear documentation
class ExampleClass:
    """Brief description of the class purpose."""
    
    def __init__(self, param: str):
        """Initialize the class with given parameter."""
        self.param = param
    
    def process_data(self, data: Dict) -> bool:
        """Process the given data and return success status."""
        # Implementation here
        pass
```

## 📝 Documentation Standards

### Code Comments
- **Document complex logic** with clear comments
- **Explain "why" not "what"** - the code should be self-explanatory
- **Use docstrings** for all functions and classes
- **Include examples** for complex functions
- **Update comments** when code changes

### Function Documentation
```python
def process_message(message: Dict, priority: str = "normal") -> bool:
    """
    Process incoming message with specified priority.
    
    Args:
        message: Dictionary containing message data
        priority: Priority level (low, normal, high, urgent)
    
    Returns:
        bool: True if processing successful, False otherwise
    
    Raises:
        ValueError: If message format is invalid
        ConnectionError: If unable to send response
    
    Example:
        >>> msg = {"content": "Hello", "from": "Agent-1"}
        >>> process_message(msg, "high")
        True
    """
    # Implementation here
    pass
```

### README Files
- **Include purpose** and usage instructions
- **List dependencies** and installation steps
- **Provide examples** of common usage
- **Document configuration** options
- **Include troubleshooting** section

## 🔧 Coding Standards

### Python Style
- **Follow PEP 8** style guidelines
- **Use meaningful variable names** - avoid single letters except for loops
- **Keep functions small** - ideally under 50 lines
- **Limit line length** to 79 characters
- **Use type hints** for function parameters and returns

### Error Handling
```python
def safe_operation(data: Dict) -> Optional[Dict]:
    """Perform operation with proper error handling."""
    try:
        # Main operation
        result = process_data(data)
        return result
    except ValueError as e:
        logger.error(f"Invalid data format: {e}")
        return None
    except ConnectionError as e:
        logger.error(f"Connection failed: {e}")
        # Retry logic here
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

### Logging Standards
- **Use appropriate log levels** (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Include context** in log messages
- **Use structured logging** when possible
- **Don't log sensitive data** like passwords or tokens
- **Log at function entry/exit** for debugging

## 🧪 Testing Standards

### Test Structure
- **Write tests for all functions** with complex logic
- **Test edge cases** and error conditions
- **Use descriptive test names** that explain what is being tested
- **Group related tests** in test classes
- **Mock external dependencies** to isolate unit tests

### Test Examples
```python
import unittest
from unittest.mock import patch, MagicMock

class TestMessageProcessor(unittest.TestCase):
    """Test cases for message processing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = MessageProcessor()
    
    def test_valid_message_processing(self):
        """Test processing of valid message."""
        message = {"content": "test", "from": "Agent-1"}
        result = self.processor.process(message)
        self.assertTrue(result)
    
    def test_invalid_message_format(self):
        """Test handling of invalid message format."""
        message = {"invalid": "format"}
        with self.assertRaises(ValueError):
            self.processor.process(message)
    
    @patch('module.external_service')
    def test_external_service_failure(self, mock_service):
        """Test handling of external service failure."""
        mock_service.side_effect = ConnectionError("Service unavailable")
        message = {"content": "test", "from": "Agent-1"}
        result = self.processor.process(message)
        self.assertFalse(result)
```

## 🔒 Security Standards

### Input Validation
- **Validate all inputs** before processing
- **Sanitize user data** to prevent injection attacks
- **Use parameterized queries** for database operations
- **Validate file paths** to prevent directory traversal
- **Check file types** before processing uploads

### Data Protection
- **Encrypt sensitive data** at rest and in transit
- **Use secure random** for cryptographic operations
- **Never store passwords** in plain text
- **Implement proper access controls** for all resources
- **Log security events** for audit purposes

### Code Security
```python
import hashlib
import secrets
from cryptography.fernet import Fernet

def secure_hash_password(password: str) -> str:
    """Securely hash password using salt."""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return salt + hash_obj.hex()

def validate_file_path(file_path: str) -> bool:
    """Validate file path to prevent directory traversal."""
    import os
    normalized_path = os.path.normpath(file_path)
    return not normalized_path.startswith('..') and not normalized_path.startswith('/')
```

## 📊 Performance Standards

### Optimization Guidelines
- **Profile code** to identify bottlenecks
- **Use appropriate data structures** for your use case
- **Cache expensive operations** when beneficial
- **Batch operations** when possible
- **Use async/await** for I/O-bound operations

### Memory Management
- **Close file handles** and database connections
- **Use context managers** for resource management
- **Avoid memory leaks** in long-running processes
- **Monitor memory usage** in production
- **Use generators** for large datasets

### Performance Monitoring
```python
import time
import logging
from functools import wraps

def performance_monitor(func):
    """Decorator to monitor function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logging.info(f"{func.__name__} completed in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logging.error(f"{func.__name__} failed after {execution_time:.2f}s: {e}")
            raise
    return wrapper
```

## 🔄 Version Control

### Commit Standards
- **Write descriptive commit messages** that explain the change
- **Keep commits atomic** - one logical change per commit
- **Use conventional commit format** when possible
- **Reference issue numbers** in commit messages
- **Test before committing** to ensure code works

### Branch Strategy
- **Use feature branches** for new development
- **Keep main branch stable** and deployable
- **Review code** before merging to main
- **Delete feature branches** after merging
- **Tag releases** with version numbers

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(api): add user authentication endpoint
fix(gui): resolve button click event handling
docs(readme): update installation instructions
test(processor): add unit tests for message validation
```

## 🚀 Deployment Standards

### Environment Configuration
- **Use environment variables** for configuration
- **Separate development/production** configurations
- **Validate configuration** at startup
- **Use secure defaults** for all settings
- **Document all configuration options**

### Deployment Checklist
- [ ] **All tests pass** in CI/CD pipeline
- [ ] **Code review completed** and approved
- [ ] **Documentation updated** for any changes
- [ ] **Configuration validated** for target environment
- [ ] **Backup procedures** in place
- [ ] **Rollback plan** prepared
- [ ] **Monitoring configured** for new deployment

---

**Version**: 2.0 (Consolidated)  
**Last Updated**: 2025-06-29  
**Next Review**: 2025-07-29 