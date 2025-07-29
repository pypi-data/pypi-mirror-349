# tests/test_optimized.py

"""
Optimized test suite for the ChatMS plugin.
Focuses on core functionality with fast, reliable tests.
"""

import asyncio
import pytest
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

# Import core components
from chatms_plugin import ChatSystem, Config, ChatType, MessageType, MessageStatus, UserRole
from chatms_plugin.exceptions import AuthenticationError, AuthorizationError, ValidationError
from chatms_plugin.models.user import UserCreate, User
from chatms_plugin.models.chat import ChatCreate, Chat
from chatms_plugin.models.message import MessageCreate, Message


class OptimizedMockDatabase:
    """Lightweight in-memory database for testing."""
    
    def __init__(self):
        self.users = {}
        self.chats = {}
        self.messages = {}
        self.user_counter = 0
        self.chat_counter = 0
        self.message_counter = 0
    
    def generate_id(self):
        """Generate a simple sequential ID."""
        return str(uuid.uuid4())
    
    async def init(self):
        pass
    
    async def close(self):
        pass
    
    # User operations
    async def create_user(self, user):
        user_id = self.generate_id()
        user_dict = user.dict()
        user_dict['id'] = user_id
        user_dict['created_at'] = datetime.now()
        self.users[user_id] = user_dict
        return User(**user_dict)
    
    async def get_user(self, user_id):
        user_data = self.users.get(user_id)
        return User(**user_data) if user_data else None
    
    async def get_user_by_username(self, username):
        for user_data in self.users.values():
            if user_data['username'] == username:
                return User(**user_data)
        return None
    
    async def update_user(self, user_id, data):
        if user_id in self.users:
            self.users[user_id].update(data)
            self.users[user_id]['updated_at'] = datetime.now()
            return User(**self.users[user_id])
        return None
    
    # Chat operations
    async def create_chat(self, chat):
        chat_id = self.generate_id()
        chat_dict = chat.dict()
        chat_dict['id'] = chat_id
        chat_dict['created_at'] = datetime.now()
        self.chats[chat_id] = chat_dict
        return Chat(**chat_dict)
    
    async def get_chat(self, chat_id):
        chat_data = self.chats.get(chat_id)
        return Chat(**chat_data) if chat_data else None
    
    async def update_chat(self, chat_id, data):
        if chat_id in self.chats:
            self.chats[chat_id].update(data)
            return Chat(**self.chats[chat_id])
        return None
    
    async def add_chat_member(self, chat_id, user_id, role):
        chat = await self.get_chat(chat_id)
        if chat:
            # Simple member addition
            return True
        return False
    
    async def remove_chat_member(self, chat_id, user_id):
        chat = await self.get_chat(chat_id)
        if chat:
            # Simple member removal
            return True
        return False
    
    async def get_user_chats(self, user_id):
        # Return chats where user is a member (simplified)
        result = []
        for chat_data in self.chats.values():
            chat = Chat(**chat_data)
            if chat.is_member(user_id):
                result.append(chat)
        return result
    
    # Message operations
    async def create_message(self, message):
        message_id = self.generate_id()
        message_dict = message.dict()
        message_dict['id'] = message_id
        message_dict['created_at'] = datetime.now()
        self.messages[message_id] = message_dict
        return Message(**message_dict)
    
    async def get_message(self, message_id):
        message_data = self.messages.get(message_id)
        return Message(**message_data) if message_data else None
    
    async def update_message(self, message_id, data):
        if message_id in self.messages:
            self.messages[message_id].update(data)
            return Message(**self.messages[message_id])
        return None
    
    async def get_chat_messages(self, chat_id, **kwargs):
        result = []
        for message_data in self.messages.values():
            if message_data['chat_id'] == chat_id:
                result.append(Message(**message_data))
        return result
    
    async def add_reaction(self, message_id, user_id, reaction_type):
        # Simplified reaction addition
        from chatms_plugin.models.message import Reaction
        return Reaction(
            id=self.generate_id(),
            user_id=user_id,
            reaction_type=reaction_type,
            created_at=datetime.now()
        )
    
    async def remove_reaction(self, message_id, user_id, reaction_type):
        return True
    
    async def search_messages(self, query, user_id, **kwargs):
        result = []
        for message_data in self.messages.values():
            if query.lower() in message_data.get('content', '').lower():
                result.append(Message(**message_data))
        return result
    
    async def get_chat_stats(self, chat_id):
        return {"chat_id": chat_id, "message_count": 0}
    
    async def get_user_stats(self, user_id):
        return {"user_id": user_id, "message_count": 0}


@pytest.fixture(scope="function")
def config():
    """Optimized test configuration."""
    return Config(
        database_type="sqlite",
        database_url="sqlite:///:memory:",
        storage_type="local",
        storage_path="/tmp/test_storage",
        jwt_secret="test-secret-key-12345",
        enable_encryption=False,  # Disable for faster tests
        max_file_size_mb=1,
        allowed_extensions=["jpg", "txt"]
    )


@pytest.fixture(scope="function")
async def chat_system(config):
    """Optimized chat system with mocked components."""
    system = ChatSystem(config)
    
    # Use optimized mock database
    system.db_handler = OptimizedMockDatabase()
    await system.db_handler.init()
    
    # Mock other components for speed
    system.storage_handler = MagicMock()
    system.storage_handler.init = AsyncMock()
    system.storage_handler.close = AsyncMock()
    system.storage_handler.save_file = AsyncMock(return_value="test/file/path.jpg")
    
    system.notification_handler = MagicMock()
    system.notification_handler.init = AsyncMock()
    system.notification_handler.close = AsyncMock()
    system.notification_handler.send_notification = AsyncMock(return_value=True)
    
    system.connection_manager = MagicMock()
    system.connection_manager.init = AsyncMock()
    system.connection_manager.close = AsyncMock()
    system.connection_manager.send_new_message = AsyncMock(return_value=True)
    system.connection_manager.send_typing_indicator = AsyncMock(return_value=True)
    
    system.analytics_service = MagicMock()
    system.analytics_service.init = AsyncMock()
    system.analytics_service.track_user_registered = AsyncMock()
    system.analytics_service.track_auth_success = AsyncMock()
    system.analytics_service.track_message = AsyncMock()
    system.analytics_service.track_chat_created = AsyncMock()
    system.analytics_service.start_timer = MagicMock()
    system.analytics_service.stop_timer = AsyncMock()
    
    # Initialize system
    await system.init()
    
    yield system
    
    # Cleanup
    await system.close()


# Core functionality tests
@pytest.mark.asyncio
async def test_user_registration_and_auth(chat_system):
    """Test user registration and authentication flow."""
    # Register user
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="Password123!",
        full_name="Test User"
    )
    
    user = await chat_system.register_user(user_data)
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    
    # Authenticate user
    token = await chat_system.authenticate_user("testuser", "Password123!")
    assert token is not None
    
    # Test invalid authentication
    with pytest.raises(AuthenticationError):
        await chat_system.authenticate_user("testuser", "WrongPassword")


@pytest.mark.asyncio
async def test_chat_creation_and_membership(chat_system):
    """Test chat creation and membership management."""
    # Create users
    user1 = await chat_system.register_user(UserCreate(
        username="user1", email="user1@test.com", password="Pass123!"
    ))
    user2 = await chat_system.register_user(UserCreate(
        username="user2", email="user2@test.com", password="Pass123!"
    ))
    
    # Create chat
    chat_data = ChatCreate(
        name="Test Chat",
        chat_type=ChatType.GROUP,
        member_ids=[user1.id, user2.id]
    )
    
    chat = await chat_system.create_chat(chat_data, user1.id)
    assert chat.id is not None
    assert chat.name == "Test Chat"
    assert len(chat.members) == 2
    
    # Test chat access
    retrieved_chat = await chat_system.get_chat(chat.id, user1.id)
    assert retrieved_chat.id == chat.id
    
    # Test unauthorized access
    user3 = await chat_system.register_user(UserCreate(
        username="user3", email="user3@test.com", password="Pass123!"
    ))
    
    with pytest.raises(AuthorizationError):
        await chat_system.get_chat(chat.id, user3.id)


@pytest.mark.asyncio
async def test_message_operations(chat_system):
    """Test message sending, updating, and operations."""
    # Setup users and chat
    user = await chat_system.register_user(UserCreate(
        username="msguser", email="msg@test.com", password="Pass123!"
    ))
    
    chat_data = ChatCreate(
        name="Message Chat",
        chat_type=ChatType.GROUP,
        member_ids=[user.id]
    )
    chat = await chat_system.create_chat(chat_data, user.id)
    
    # Send message
    message_data = MessageCreate(
        chat_id=chat.id,
        content="Hello, world!",
        message_type=MessageType.TEXT
    )
    
    message = await chat_system.send_message(user.id, message_data)
    assert message.id is not None
    assert message.content == "Hello, world!"
    assert message.sender_id == user.id
    
    # Get chat messages
    messages = await chat_system.get_chat_messages(chat.id, user.id)
    assert len(messages) >= 1
    assert any(m.id == message.id for m in messages)
    
    # Add reaction
    reaction = await chat_system.add_reaction(message.id, user.id, "👍")
    assert reaction is not None
    
    # Remove reaction
    result = await chat_system.remove_reaction(message.id, user.id, "👍")
    assert result is True


@pytest.mark.asyncio
async def test_file_operations(chat_system):
    """Test file upload and file message operations."""
    # Setup
    user = await chat_system.register_user(UserCreate(
        username="fileuser", email="file@test.com", password="Pass123!"
    ))
    
    chat_data = ChatCreate(
        name="File Chat",
        chat_type=ChatType.GROUP,
        member_ids=[user.id]
    )
    chat = await chat_system.create_chat(chat_data, user.id)
    
    # Upload file
    file_data = b"test file content"
    file_url = await chat_system.upload_file(
        chat_id=chat.id,
        user_id=user.id,
        file_data=file_data,
        file_name="test.txt",
        content_type="text/plain"
    )
    
    assert file_url is not None
    
    # Send file message
    file_message = await chat_system.send_file_message(
        sender_id=user.id,
        chat_id=chat.id,
        file_url=file_url,
        file_name="test.txt",
        content_type="text/plain",
        caption="Test file"
    )
    
    assert file_message is not None
    assert file_message.message_type == MessageType.FILE


@pytest.mark.asyncio
async def test_real_time_features(chat_system):
    """Test real-time features like typing indicators."""
    # Setup
    user = await chat_system.register_user(UserCreate(
        username="realtimeuser", email="realtime@test.com", password="Pass123!"
    ))
    
    chat_data = ChatCreate(
        name="Realtime Chat",
        chat_type=ChatType.GROUP,
        member_ids=[user.id]
    )
    chat = await chat_system.create_chat(chat_data, user.id)
    
    # Send typing indicator
    result = await chat_system.send_typing_indicator(chat.id, user.id, True)
    assert result is True
    
    # Stop typing
    result = await chat_system.send_typing_indicator(chat.id, user.id, False)
    assert result is True


@pytest.mark.asyncio
async def test_search_functionality(chat_system):
    """Test message search functionality."""
    # Setup
    user = await chat_system.register_user(UserCreate(
        username="searchuser", email="search@test.com", password="Pass123!"
    ))
    
    chat_data = ChatCreate(
        name="Search Chat",
        chat_type=ChatType.GROUP,
        member_ids=[user.id]
    )
    chat = await chat_system.create_chat(chat_data, user.id)
    
    # Send searchable message
    message_data = MessageCreate(
        chat_id=chat.id,
        content="This is a unique searchable message",
        message_type=MessageType.TEXT
    )
    await chat_system.send_message(user.id, message_data)
    
    # Search for message
    results = await chat_system.search_messages(user.id, "unique searchable")
    assert len(results) >= 1
    assert any("unique searchable" in msg.content for msg in results)


@pytest.mark.asyncio
async def test_error_handling(chat_system):
    """Test error handling and validation."""
    # Test invalid user registration
    with pytest.raises(ValidationError):
        await chat_system.register_user(UserCreate(
            username="",  # Invalid empty username
            email="invalid@test.com",
            password="Pass123!"
        ))
    
    # Test accessing non-existent chat
    user = await chat_system.register_user(UserCreate(
        username="erroruser", email="error@test.com", password="Pass123!"
    ))
    
    fake_chat_id = str(uuid.uuid4())
    retrieved_chat = await chat_system.get_chat(fake_chat_id, user.id)
    assert retrieved_chat is None


@pytest.mark.asyncio
async def test_concurrent_operations(chat_system):
    """Test concurrent operations for race conditions."""
    # Create multiple users concurrently
    tasks = []
    for i in range(5):
        user_data = UserCreate(
            username=f"concurrent_user_{i}",
            email=f"concurrent{i}@test.com",
            password="Pass123!"
        )
        tasks.append(chat_system.register_user(user_data))
    
    users = await asyncio.gather(*tasks)
    assert len(users) == 5
    assert all(user.id is not None for user in users)
    
    # Create chat with all users
    chat_data = ChatCreate(
        name="Concurrent Chat",
        chat_type=ChatType.GROUP,
        member_ids=[user.id for user in users]
    )
    chat = await chat_system.create_chat(chat_data, users[0].id)
    
    # Send messages concurrently
    message_tasks = []
    for i, user in enumerate(users):
        message_data = MessageCreate(
            chat_id=chat.id,
            content=f"Concurrent message {i}",
            message_type=MessageType.TEXT
        )
        message_tasks.append(chat_system.send_message(user.id, message_data))
    
    messages = await asyncio.gather(*message_tasks)
    assert len(messages) == 5
    assert all(msg.id is not None for msg in messages)


# Performance test
@pytest.mark.asyncio
async def test_performance_benchmark(chat_system):
    """Basic performance benchmark test."""
    import time
    
    # Measure user registration performance
    start_time = time.time()
    
    users = []
    for i in range(10):
        user_data = UserCreate(
            username=f"perf_user_{i}",
            email=f"perf{i}@test.com",
            password="Pass123!"
        )
        user = await chat_system.register_user(user_data)
        users.append(user)
    
    registration_time = time.time() - start_time
    
    # Measure message sending performance
    chat_data = ChatCreate(
        name="Performance Chat",
        chat_type=ChatType.GROUP,
        member_ids=[user.id for user in users[:3]]
    )
    chat = await chat_system.create_chat(chat_data, users[0].id)
    
    start_time = time.time()
    
    for i in range(20):
        message_data = MessageCreate(
            chat_id=chat.id,
            content=f"Performance message {i}",
            message_type=MessageType.TEXT
        )
        await chat_system.send_message(users[0].id, message_data)
    
    messaging_time = time.time() - start_time
    
    # Basic performance assertions (adjust thresholds as needed)
    assert registration_time < 2.0, f"User registration too slow: {registration_time}s"
    assert messaging_time < 1.0, f"Message sending too slow: {messaging_time}s"
    
    print(f"Performance metrics:")
    print(f"- User registration (10 users): {registration_time:.3f}s")
    print(f"- Message sending (20 messages): {messaging_time:.3f}s")


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "--tb=short"])