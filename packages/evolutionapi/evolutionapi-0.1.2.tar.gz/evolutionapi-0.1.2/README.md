# Evolution Client Python

Python client to interact with the Evolution API.

## Installation

```bash
pip install evolutionapi
```

## Basic Usage

### Initializing the Client

```python
from evolutionapi.client import EvolutionClient

client = EvolutionClient(
    base_url='http://your-server:port',
    api_token='your-api-token'
)
```

## Features

- **Instance Management** - Create, configure and manage instances
- **Messaging** - Send text, media, buttons, lists, locations, and more
- **Group Management** - Create groups, manage participants, settings
- **Profile Management** - Update name, status, photo, privacy settings
- **WebSocket Support** - Real-time event handling
- **Type-Safe Event Processing** - Webhook and WebSocket event handling with IDE autocomplete

## Core Features

### Instance Management

```python
# Create instance
from evolutionapi.models.instance import InstanceConfig

config = InstanceConfig(
    instanceName="my-instance",
    integration="WHATSAPP-BAILEYS",
    qrcode=True
)

new_instance = client.instances.create_instance(config)

# Get QR code
qr_code = client.instances.get_instance_qrcode(instance_id, instance_token)
```

### Sending Messages

```python
# Text message
from evolutionapi.models.message import TextMessage

message = TextMessage(
    number="5511999999999",
    text="Hello, how are you?"
)

response = client.messages.send_text(instance_id, message, instance_token)

# Media message
from evolutionapi.models.message import MediaMessage, MediaType

message = MediaMessage(
    number="5511999999999",
    mediatype=MediaType.IMAGE.value,
    mimetype="image/jpeg",
    caption="My image",
    media="base64_of_image_or_url"
)

response = client.messages.send_media(instance_id, message, instance_token)
```

### Group Management

```python
# Create group
from evolutionapi.models.group import CreateGroup

config = CreateGroup(
    subject="Group Name",
    participants=["5511999999999", "5511888888888"]
)

response = client.group.create_group(instance_id, config, instance_token)

# Add participants
from evolutionapi.models.group import UpdateParticipant

config = UpdateParticipant(
    action="add",
    participants=["5511999999999"]
)

response = client.group.update_participant(instance_id, "group_jid", config, instance_token)
```

## WebSocket & Event Processing

### Setting Up WebSocket

```python
# Configure WebSocket
from evolutionapi.models.websocket import WebSocketConfig

websocket_config = WebSocketConfig(
    enabled=True,
    events=["MESSAGES_UPSERT", "QRCODE_UPDATED", "CONNECTION_UPDATE"]
)

client.websocket.set_websocket(instance_id, websocket_config, instance_token)

# Create WebSocket manager
websocket = client.create_websocket(
    instance_id=instance_id,
    api_token=instance_token
)
```

### Event Processing System

The Evolution API client includes a typing system for WebSocket and webhook events with proper IDE autocomplete support:

#### Type-Safe Event Handlers

```python
from evolutionapi.typing import (
    WebhookEventProcessor,
    MessageEventDict,  # For message events
    MessageUpdateEventDict,  # For message status updates
    ConnectionEventDict,  # For connection status changes
    EVENT_MESSAGE_UPSERT,
    EVENT_MESSAGE_UPDATE,
    EVENT_CONNECTION_UPDATE
)

# Create event processor
event_processor = WebhookEventProcessor(client)

# Message event handler with attribute access
def on_message(event: MessageEventDict):
    # Convert to MessageWrapper for dot-notation access
    message = client.convert_message(event.data)
    if not message:
        return
        
    # Access using dot notation instead of data["key"]["remoteJid"]
    sender = message.key.remoteJid
    
    # Access message content based on type
    if message.messageType == "conversation":
        text = message.message.conversation
        print(f"Text from {sender}: {text}")

# Register handlers
event_processor.register(EVENT_MESSAGE_UPSERT, on_message)
event_processor.register(EVENT_MESSAGE_UPDATE, on_message_update)
event_processor.register(EVENT_CONNECTION_UPDATE, on_connection)

# Connect WebSocket to event processor
def ws_message_handler(data):
    event_processor.process_event(data)

websocket.on('messages.upsert', ws_message_handler)
websocket.connect()
```

### Key Benefits of Typing System

- Access data with dot notation (`event.data.state` instead of `event["data"]["state"]`)
- Type-specific event handlers with proper IDE autocomplete
- Uniform processing of both webhook and WebSocket events
- Strongly typed event data for better development experience

For complete documentation and more examples, see the extended documentation.

## Additional Features

- **Chat Operations** - Check WhatsApp numbers, mark messages as read, archive chats
- **Call Simulation** - Simulate incoming calls
- **Label Management** - Add/remove message labels
- **Media Handling** - Download media from messages
- **Status Updates** - Send status updates with text, images, or videos

## Usage Tips

1. Always use try/except blocks when connecting to WebSocket
2. Keep your API token secure and don't expose it in logs
3. Check Evolution API documentation for endpoint-specific details
4. Use logging for debugging and monitoring
