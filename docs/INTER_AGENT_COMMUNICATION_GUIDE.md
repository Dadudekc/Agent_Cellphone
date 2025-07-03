# Inter-Agent Communication Guide
## Dream.OS Agent Coordination Protocol

### Problem Statement

The Dream.OS system uses a single shared cursor and keyboard for agent communication. This creates a critical limitation:

- **Single Point of Control**: Only one agent can control the input at any given time
- **Simultaneous Access Conflicts**: Multiple agents trying to send messages simultaneously will cause:
  - Lost or garbled input
  - Interrupted message transmission
  - System instability
  - Unpredictable behavior

### Solution: Message Queue Protocol

To ensure reliable communication, we implement a **Message Queue Protocol** that serializes all agent communications.

## Protocol Overview

### Core Principles

1. **Single Agent Control**: Only one agent may use the cursor/keyboard at a time
2. **Queue-Based Communication**: All outgoing messages must be queued
3. **Sequential Processing**: Messages are processed in FIFO (First In, First Out) order
4. **Acknowledgment Required**: Agents must acknowledge receipt and completion
5. **Audit Trail**: All communications are logged for traceability

### Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Agent-1   │    │   Agent-2   │    │   Agent-N   │
│             │    │             │    │             │
│  Inbox/     │    │  Inbox/     │    │  Inbox/     │
│  Outbox/    │    │  Outbox/    │    │  Outbox/    │
└─────┬───────┘    └─────┬───────┘    └─────┬───────┘
      │                  │                  │
      └──────────────────┼──────────────────┘
                         │
              ┌──────────▼──────────┐
              │   Message Queue     │
              │   (FIFO System)     │
              │                     │
              │  queue/             │
              │  ├── pending/       │
              │  ├── processing/    │
              │  ├── completed/     │
              │  └── lock           │
              └─────────────────────┘
                         │
              ┌──────────▼──────────┐
              │   Queue Manager     │
              │   (Single Process)  │
              └─────────────────────┘
                         │
              ┌──────────▼──────────┐
              │   Cursor/Keyboard   │
              │   (Shared Resource) │
              └─────────────────────┘
```

## Message Queue Structure

### Directory Layout

```
agent_workspaces/
├── queue/
│   ├── pending/           # Messages waiting to be sent
│   ├── processing/        # Currently being sent
│   ├── completed/         # Successfully sent
│   ├── failed/           # Failed to send
│   ├── lock              # Lock file (exists = busy)
│   └── queue.log         # Audit log
├── Agent-1/
│   ├── inbox/            # Received messages
│   ├── outbox/           # Sent messages
│   └── status.json       # Current status
├── Agent-2/
│   ├── inbox/
│   ├── outbox/
│   └── status.json
└── ...
```

### Message Format

Each message is stored as a JSON file with the following structure:

```json
{
  "id": "2024-07-02T12-00-00_agent-2_to_agent-1_001",
  "timestamp": "2024-07-02T12:00:00.000Z",
  "from": "agent-2",
  "to": "agent-1",
  "message": "Hello Agent-1! I'm coordinating our data analysis project.",
  "tag": "coordinate",
  "priority": "normal",
  "status": "pending",
  "retries": 0,
  "max_retries": 3,
  "created_at": "2024-07-02T12:00:00.000Z",
  "processed_at": null,
  "completed_at": null,
  "error": null
}
```

### Status Values

- `pending`: Message is queued and waiting
- `processing`: Message is currently being sent
- `completed`: Message was successfully sent
- `failed`: Message failed to send (after retries)
- `acknowledged`: Recipient has acknowledged receipt

## Communication Workflow

### 1. Sending a Message

```python
# Agent wants to send a message
def send_message(to_agent, message, tag="normal", priority="normal"):
    # 1. Create message object
    msg = {
        "id": generate_message_id(),
        "timestamp": datetime.now().isoformat(),
        "from": self.agent_id,
        "to": to_agent,
        "message": message,
        "tag": tag,
        "priority": priority,
        "status": "pending",
        "retries": 0,
        "max_retries": 3,
        "created_at": datetime.now().isoformat(),
        "processed_at": None,
        "completed_at": None,
        "error": None
    }
    
    # 2. Write to queue
    queue_file = f"queue/pending/{msg['id']}.json"
    with open(queue_file, 'w') as f:
        json.dump(msg, f, indent=2)
    
    # 3. Log the action
    log_action("enqueue", msg)
    
    return msg['id']
```

### 2. Queue Processing

The Queue Manager processes messages in order:

```python
def process_queue():
    while True:
        # 1. Check for lock
        if os.path.exists("queue/lock"):
            time.sleep(1)
            continue
        
        # 2. Get next message
        pending_files = sorted(os.listdir("queue/pending"))
        if not pending_files:
            time.sleep(1)
            continue
        
        # 3. Acquire lock
        with open("queue/lock", 'w') as f:
            f.write(f"Processing: {pending_files[0]}")
        
        # 4. Process message
        process_message(pending_files[0])
        
        # 5. Release lock
        os.remove("queue/lock")
```

### 3. Receiving Messages

```python
def check_inbox():
    """Check for new messages in inbox"""
    inbox_dir = f"agent_workspaces/{self.agent_id}/inbox"
    new_messages = []
    
    for file in os.listdir(inbox_dir):
        if file.endswith('.json'):
            with open(os.path.join(inbox_dir, file), 'r') as f:
                msg = json.load(f)
                if msg['status'] == 'completed':
                    new_messages.append(msg)
    
    return new_messages

def acknowledge_message(message_id):
    """Acknowledge receipt of a message"""
    # Update message status
    # Move to acknowledged folder
    # Send acknowledgment back to sender
```

## Best Practices

### For Agent Developers

1. **Always Use the Queue**: Never bypass the queue system
2. **Check Inbox Regularly**: Poll for new messages every 30 seconds
3. **Acknowledge Messages**: Always acknowledge receipt of important messages
4. **Handle Failures**: Implement retry logic for failed messages
5. **Log Everything**: Maintain detailed logs of all communications

### Message Priority Levels

- `critical`: System-level messages (restart, emergency stop)
- `high`: Important coordination messages
- `normal`: Regular communication
- `low`: Non-urgent updates

### Error Handling

1. **Message Timeout**: Messages older than 5 minutes are marked as failed
2. **Retry Logic**: Failed messages are retried up to 3 times
3. **Dead Letter Queue**: Messages that fail after retries go to `queue/failed/`
4. **System Recovery**: Queue manager can recover from crashes

## Implementation Examples

### Basic Agent Communication

```python
# Agent-2 sending to Agent-1
queue_manager = MessageQueueManager("agent-2")

# Send a coordination message
msg_id = queue_manager.send_message(
    to_agent="agent-1",
    message="Hello Agent-1! Ready to coordinate?",
    tag="coordinate",
    priority="normal"
)

# Check for responses
responses = queue_manager.check_inbox()
for response in responses:
    print(f"Received: {response['message']}")
    queue_manager.acknowledge_message(response['id'])
```

### Queue Manager Usage

```bash
# Start the queue manager
python queue_manager.py --mode 2-agent --log-level INFO

# Monitor queue status
python queue_manager.py --status

# Process queue manually
python queue_manager.py --process-now
```

## Monitoring and Debugging

### Queue Status Commands

```bash
# Check queue status
python queue_manager.py --status

# View pending messages
python queue_manager.py --list-pending

# View failed messages
python queue_manager.py --list-failed

# Clear failed messages
python queue_manager.py --clear-failed
```

### Log Analysis

```bash
# View recent activity
tail -f agent_workspaces/queue/queue.log

# Search for specific agent
grep "agent-1" agent_workspaces/queue/queue.log

# Check for errors
grep "ERROR" agent_workspaces/queue/queue.log
```

## Security Considerations

1. **Message Validation**: Validate all incoming messages
2. **Rate Limiting**: Prevent message flooding
3. **Authentication**: Verify sender identity (future enhancement)
4. **Encryption**: Encrypt sensitive messages (future enhancement)

## Future Enhancements

1. **Real-time Notifications**: WebSocket-based real-time updates
2. **Message Encryption**: End-to-end encryption for sensitive communications
3. **Load Balancing**: Multiple queue managers for high-volume systems
4. **Message Persistence**: Database storage for message history
5. **API Interface**: REST API for external system integration

## Conclusion

The Message Queue Protocol ensures reliable, ordered, and traceable communication between agents while preventing cursor/keyboard conflicts. This system provides the foundation for scalable multi-agent coordination in the Dream.OS environment.

For implementation details, see the accompanying `queue_manager.py` script and example agent integration code. 