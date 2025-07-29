# tests/lightweight_mocks.py

"""
Lightweight mocks for optimized testing.
These mocks provide minimal functionality needed for testing without heavy dependencies.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock

from chatms_plugin.models.user import User, UserInChat
from chatms_plugin.models.chat import Chat
from chatms_plugin.models.message import Message, Reaction
from chatms_plugin.config import UserRole, MessageStatus, MessageType


class LightweightSecurityManager:
    """Lightweight security manager for testing."""
    
    def __init__(self, config):
        self.config = config
    
    async def hash_password(self, password: str) -> str:
        """Simple hash for testing - just prefix with 'hashed_'."""
        return f"hashed_{password}"
    
    async def verify_password(self, password: str, hashed_password: str) -> bool:
        """Simple verification for testing."""
        return hashed_password == f"hashed_{password}"
    
    async def create_token(self, user_id: str, expires_minutes: int = None) -> str:
        """Create a simple token for testing."""
        return f"token_{user_id}_{uuid.uuid4().hex[:8]}"
    
    async def get_user_id_from_token(self, token: str) -> str:
        """Extract user ID from token."""
        if token.startswith("token_"):
            parts = token.split("_")
            if len(parts) >= 2:
                return parts[1]
        raise ValueError("Invalid token")
    
    async def encrypt(self, data: str) -> str:
        """Simple encryption for testing - just reverse the string."""
        return data[::-1]
    
    async def decrypt(self, encrypted_data: str) -> str:
        """Simple decryption for testing - reverse back."""
        return encrypted_data[::-1]


class LightweightConnectionManager:
    """Lightweight connection manager for testing."""
    
    def __init__(self, config):
        self.config = config
        self.connections = {}
        self.user_connections = {}
    
    async def init(self):
        pass
    
    async def close(self):
        pass
    
    async def connect(self, websocket, user_id: str):
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(websocket)
    
    async def disconnect(self, websocket, user_id: str):
        if user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
    
    async def send_new_message(self, user_id: str, message_data: Dict) -> bool:
        return True
    
    async def send_typing_indicator(self, user_id: str, typing_data: Dict) -> bool:
        return True
    
    async def send_message_updated(self, user_id: str, message_data: Dict) -> bool:
        return True
    
    async def send_chat_member_added(self, chat_id: str, user_id: str, chat_data: Dict):
        pass
    
    async def send_chat_member_removed(self, chat_id: str, user_id: str, chat_data: Dict):
        pass
    
    async def send_message_deleted(self, user_id: str, delete_data: Dict) -> bool:
        return True
    
    async def send_reaction_added(self, user_id: str, reaction_data: Dict) -> bool:
        return True
    
    async def send_reaction_removed(self, user_id: str, reaction_data: Dict) -> bool:
        return True
    
    async def send_message_pinned(self, user_id: str, pin_data: Dict) -> bool:
        return True
    
    async def send_message_unpinned(self, user_id: str, unpin_data: Dict) -> bool:
        return True
    
    async def send_messages_read(self, user_id: str, read_data: Dict) -> bool:
        return True
    
    async def update_presence(self, presence_data: Dict):
        pass


class LightweightAnalyticsService:
    """Lightweight analytics service for testing."""
    
    def __init__(self, config):
        self.config = config
        self.events = []
    
    async def init(self, redis=None):
        pass
    
    async def track_user_registered(self, user_id: str):
        self.events.append(("user_registered", user_id))
    
    async def track_auth_success(self, user_id: str):
        self.events.append(("auth_success", user_id))
    
    async def track_auth_failure(self, username: str, reason: str):
        self.events.append(("auth_failure", username, reason))
    
    async def track_message(self, message_id: str, chat_id: str, sender_id: str, 
                          message_type: str, size: int):
        self.events.append(("message", message_id, chat_id, sender_id, message_type, size))
    
    async def track_chat_created(self, chat_id: str, creator_id: str, chat_type: str):
        self.events.append(("chat_created", chat_id, creator_id, chat_type))
    
    def start_timer(self, timer_name: str):
        pass
    
    async def stop_timer(self, timer_name: str, additional_data: Dict = None) -> Optional[float]:
        return 0.001  # Return a small duration


class LightweightStorageHandler:
    """Lightweight storage handler for testing."""
    
    def __init__(self, config):
        self.config = config
        self.files = {}  # file_path -> file_data
    
    async def init(self):
        pass
    
    async def close(self):
        pass
    
    async def save_file(self, file_data: bytes, file_name: str, 
                       content_type: Optional[str] = None) -> str:
        """Save file and return a mock path."""
        file_path = f"test/{uuid.uuid4().hex}/{file_name}"
        self.files[file_path] = file_data
        return file_path
    
    async def get_file(self, file_path: str) -> Optional[bytes]:
        """Get file data."""
        return self.files.get(file_path)
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete file."""
        if file_path in self.files:
            del self.files[file_path]
            return True
        return False
    
    async def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get file information."""
        if file_path in self.files:
            return {
                "name": file_path.split("/")[-1],
                "path": file_path,
                "size": len(self.files[file_path]),
                "content_type": "application/octet-stream",
                "created_at": datetime.now().isoformat()
            }
        return None
    
    async def get_file_url(self, file_path: str, expires_in: int = 3600) -> str:
        """Get file URL."""
        return f"https://test-storage.example.com/{file_path}"
    
    async def create_thumbnail(self, file_path: str, width: int, height: int) -> Optional[str]:
        """Create thumbnail."""
        if file_path in self.files:
            thumbnail_path = f"{file_path}_thumb_{width}x{height}"
            self.files[thumbnail_path] = b"thumbnail_data"
            return thumbnail_path
        return None
    
    async def validate_file(self, file_data: bytes, file_name: str, 
                          max_size_mb: int, allowed_extensions: List[str]):
        """Validate file (simplified for testing)."""
        # Check size
        max_size_bytes = max_size_mb * 1024 * 1024
        if len(file_data) > max_size_bytes:
            from chatms_plugin.exceptions import FileSizeError
            raise FileSizeError(
                file_name=file_name,
                file_size=len(file_data),
                max_size=max_size_bytes
            )
        
        # Check extension
        import os
        _, ext = os.path.splitext(file_name)
        ext = ext.lstrip(".").lower()
        
        if allowed_extensions and ext not in [e.lower() for e in allowed_extensions]:
            from chatms_plugin.exceptions import FileTypeError
            raise FileTypeError(
                file_name=file_name,
                file_type=ext,
                allowed_types=allowed_extensions
            )


class LightweightNotificationHandler:
    """Lightweight notification handler for testing."""
    
    def __init__(self, config):
        self.config = config
        self.notifications = []
    
    async def init(self):
        pass
    
    async def close(self):
        pass
    
    async def send_notification(self, user_id: str, title: str, body: str, 
                              data: Optional[Dict[str, Any]] = None) -> bool:
        """Record notification for testing."""
        self.notifications.append({
            "user_id": user_id,
            "title": title,
            "body": body,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        return True


class MemoryDatabase:
    """Complete in-memory database for fast testing."""
    
    def __init__(self, config):
        self.config = config
        self.users = {}
        self.chats = {}
        self.messages = {}
        self.reactions = {}
    
    async def init(self):
        pass
    
    async def close(self):
        pass
    
    def _generate_id(self) -> str:
        return str(uuid.uuid4())
    
    # User operations
    async def create_user(self, user: User) -> User:
        user_id = self._generate_id()
        user_dict = user.dict()
        user_dict['id'] = user_id
        user_dict['created_at'] = datetime.now()
        user_dict['updated_at'] = datetime.now()
        
        self.users[user_id] = user_dict
        return User(**user_dict)
    
    async def get_user(self, user_id: str) -> Optional[User]:
        user_data = self.users.get(user_id)
        return User(**user_data) if user_data else None
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        for user_data in self.users.values():
            if user_data.get('username') == username:
                return User(**user_data)
        return None
    
    async def update_user(self, user_id: str, data: Dict[str, Any]) -> Optional[User]:
        if user_id in self.users:
            self.users[user_id].update(data)
            self.users[user_id]['updated_at'] = datetime.now()
            return User(**self.users[user_id])
        return None
    
    async def delete_user(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    # Chat operations
    async def create_chat(self, chat: Chat) -> Chat:
        chat_id = self._generate_id()
        chat_dict = chat.dict()
        chat_dict['id'] = chat_id
        chat_dict['created_at'] = datetime.now()
        chat_dict['updated_at'] = datetime.now()
        
        self.chats[chat_id] = chat_dict
        return Chat(**chat_dict)
    
    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        chat_data = self.chats.get(chat_id)
        return Chat(**chat_data) if chat_data else None
    
    async def update_chat(self, chat_id: str, data: Dict[str, Any]) -> Optional[Chat]:
        if chat_id in self.chats:
            self.chats[chat_id].update(data)
            self.chats[chat_id]['updated_at'] = datetime.now()
            return Chat(**self.chats[chat_id])
        return None
    
    async def delete_chat(self, chat_id: str) -> bool:
        if chat_id in self.chats:
            del self.chats[chat_id]
            # Also delete related messages
            messages_to_delete = [msg_id for msg_id, msg_data in self.messages.items() 
                                if msg_data.get('chat_id') == chat_id]
            for msg_id in messages_to_delete:
                del self.messages[msg_id]
            return True
        return False
    
    async def get_user_chats(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Chat]:
        result = []
        for chat_data in list(self.chats.values())[skip:skip+limit]:
            chat = Chat(**chat_data)
            if chat.is_member(user_id):
                result.append(chat)
        return result
    
    async def add_chat_member(self, chat_id: str, user_id: str, role: str) -> bool:
        chat = await self.get_chat(chat_id)
        if chat and not chat.is_member(user_id):
            chat.add_member(user_id, UserRole(role))
            await self.update_chat(chat_id, {"members": [m.dict() for m in chat.members]})
            return True
        return False
    
    async def remove_chat_member(self, chat_id: str, user_id: str) -> bool:
        chat = await self.get_chat(chat_id)
        if chat and chat.is_member(user_id):
            chat.remove_member(user_id)
            await self.update_chat(chat_id, {"members": [m.dict() for m in chat.members]})
            return True
        return False
    
    # Message operations
    async def create_message(self, message: Message) -> Message:
        message_id = self._generate_id()
        message_dict = message.dict()
        message_dict['id'] = message_id
        message_dict['created_at'] = datetime.now()
        message_dict['updated_at'] = datetime.now()
        
        self.messages[message_id] = message_dict
        return Message(**message_dict)
    
    async def get_message(self, message_id: str) -> Optional[Message]:
        message_data = self.messages.get(message_id)
        return Message(**message_data) if message_data else None
    
    async def update_message(self, message_id: str, data: Dict[str, Any]) -> Optional[Message]:
        if message_id in self.messages:
            self.messages[message_id].update(data)
            self.messages[message_id]['updated_at'] = datetime.now()
            return Message(**self.messages[message_id])
        return None
    
    async def delete_message(self, message_id: str, delete_for_everyone: bool = False) -> bool:
        if message_id in self.messages:
            if delete_for_everyone:
                del self.messages[message_id]
            else:
                self.messages[message_id]['is_deleted'] = True
            return True
        return False
    
    async def get_chat_messages(self, chat_id: str, before_id: Optional[str] = None,
                               after_id: Optional[str] = None, skip: int = 0, 
                               limit: int = 50) -> List[Message]:
        result = []
        for message_data in self.messages.values():
            if message_data.get('chat_id') == chat_id and not message_data.get('is_deleted', False):
                result.append(Message(**message_data))
        
        # Sort by creation time (most recent first)
        result.sort(key=lambda x: x.created_at, reverse=True)
        
        # Apply pagination
        return result[skip:skip+limit]
    
    # Reaction operations
    async def add_reaction(self, message_id: str, user_id: str, reaction_type: str) -> Optional[Reaction]:
        reaction_id = self._generate_id()
        reaction = Reaction(
            id=reaction_id,
            user_id=user_id,
            reaction_type=reaction_type,
            created_at=datetime.now()
        )
        
        self.reactions[reaction_id] = reaction.dict()
        
        # Add reaction to message
        if message_id in self.messages:
            reactions = self.messages[message_id].get('reactions', [])
            reactions.append(reaction.dict())
            self.messages[message_id]['reactions'] = reactions
        
        return reaction
    
    async def remove_reaction(self, message_id: str, user_id: str, reaction_type: str) -> bool:
        if message_id in self.messages:
            reactions = self.messages[message_id].get('reactions', [])
            updated_reactions = [
                r for r in reactions 
                if not (r.get('user_id') == user_id and r.get('reaction_type') == reaction_type)
            ]
            self.messages[message_id]['reactions'] = updated_reactions
            return len(updated_reactions) < len(reactions)
        return False
    
    # Search operations
    async def search_messages(self, query: str, user_id: str, chat_id: Optional[str] = None,
                             skip: int = 0, limit: int = 20) -> List[Message]:
        result = []
        for message_data in self.messages.values():
            content = message_data.get('content', '').lower()
            if query.lower() in content:
                if chat_id is None or message_data.get('chat_id') == chat_id:
                    result.append(Message(**message_data))
        
        return result[skip:skip+limit]
    
    # Stats operations
    async def get_chat_stats(self, chat_id: str) -> Dict[str, Any]:
        message_count = sum(1 for msg in self.messages.values() 
                          if msg.get('chat_id') == chat_id)
        
        return {
            "chat_id": chat_id,
            "message_count": message_count,
            "member_count": len(self.chats.get(chat_id, {}).get('members', [])),
            "created_at": self.chats.get(chat_id, {}).get('created_at', datetime.now()).isoformat()
        }
    
    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        message_count = sum(1 for msg in self.messages.values() 
                          if msg.get('sender_id') == user_id)
        
        chat_count = sum(1 for chat_data in self.chats.values()
                        for member in chat_data.get('members', [])
                        if member.get('user_id') == user_id)
        
        return {
            "user_id": user_id,
            "message_count": message_count,
            "chat_count": chat_count,
            "registration_date": self.users.get(user_id, {}).get('created_at', datetime.now()).isoformat()
        }


def create_lightweight_chat_system(config):
    """Create a chat system with lightweight mocks for testing."""
    from chatms_plugin.core.chat_system import ChatSystem
    
    system = ChatSystem(config)
    
    # Replace with lightweight implementations
    system.db_handler = MemoryDatabase(config)
    system.storage_handler = LightweightStorageHandler(config)
    system.security_manager = LightweightSecurityManager(config)
    system.connection_manager = LightweightConnectionManager(config)
    system.analytics_service = LightweightAnalyticsService(config)
    system.notification_handler = LightweightNotificationHandler(config)
    
    return system