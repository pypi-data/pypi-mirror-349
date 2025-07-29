# tests/mocks.py

"""
Mock implementations for testing the ChatMS plugin.
"""

import asyncio
import datetime
import uuid
from typing import Any, Dict, List, Optional, Union
from unittest.mock import AsyncMock, MagicMock

# Fix the import - use absolute import instead of relative
from chatms_plugin.config import Config, UserRole
from chatms_plugin.database.base import DatabaseHandler
from chatms_plugin.models.user import User, UserInChat
from chatms_plugin.models.chat import Chat
from chatms_plugin.models.message import Message, Reaction


class MockDatabaseHandler(DatabaseHandler):
    """Mock database handler for testing."""
    
    def __init__(self, config: Config):
        """Initialize the mock database handler.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.users: Dict[str, User] = {}
        self.chats: Dict[str, Chat] = {}
        self.messages: Dict[str, Message] = {}
        self.user_by_username: Dict[str, User] = {}
    
    async def init(self) -> None:
        """Initialize the database connection."""
        pass
    
    async def close(self) -> None:
        """Close the database connection."""
        pass
    
    async def create(self, model) -> Any:
        """Create a new record in the database."""
        if not hasattr(model, 'id') or not model.id:
            model.id = str(uuid.uuid4())
        
        model.created_at = datetime.datetime.now()
        model.updated_at = datetime.datetime.now()
        
        if isinstance(model, User):
            return await self.create_user(model)
        elif isinstance(model, Chat):
            return await self.create_chat(model)
        elif isinstance(model, Message):
            return await self.create_message(model)
        
        return model
    
    async def get(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        """Get a record by ID."""
        if collection == "users" and id in self.users:
            return self.users[id].dict()
        elif collection == "chats" and id in self.chats:
            return self.chats[id].dict()
        elif collection == "messages" and id in self.messages:
            return self.messages[id].dict()
        return None
    
    async def update(self, collection: str, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record by ID."""
        if collection == "users" and id in self.users:
            user = self.users[id]
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.datetime.now()
            return user.dict()
        elif collection == "chats" and id in self.chats:
            chat = self.chats[id]
            for key, value in data.items():
                if hasattr(chat, key):
                    setattr(chat, key, value)
            chat.updated_at = datetime.datetime.now()
            return chat.dict()
        elif collection == "messages" and id in self.messages:
            message = self.messages[id]
            for key, value in data.items():
                if hasattr(message, key):
                    setattr(message, key, value)
            message.updated_at = datetime.datetime.now()
            return message.dict()
        return None
    
    async def delete(self, collection: str, id: str) -> bool:
        """Delete a record by ID."""
        if collection == "users" and id in self.users:
            del self.users[id]
            return True
        elif collection == "chats" and id in self.chats:
            del self.chats[id]
            return True
        elif collection == "messages" and id in self.messages:
            del self.messages[id]
            return True
        return False
    
    async def list(self, collection: str, filters: Dict[str, Any] = None, 
                   skip: int = 0, limit: int = 100, 
                   sort: Dict[str, int] = None) -> List[Dict[str, Any]]:
        """List records with optional filtering, pagination, and sorting."""
        results = []
        
        if collection == "users":
            for user in self.users.values():
                if self._matches_filters(user.dict(), filters):
                    results.append(user.dict())
        elif collection == "chats":
            for chat in self.chats.values():
                if self._matches_filters(chat.dict(), filters):
                    results.append(chat.dict())
        elif collection == "messages":
            for message in self.messages.values():
                if self._matches_filters(message.dict(), filters):
                    results.append(message.dict())
        
        # Apply pagination
        return results[skip:skip + limit]
    
    async def count(self, collection: str, filters: Dict[str, Any] = None) -> int:
        """Count records with optional filtering."""
        results = await self.list(collection, filters)
        return len(results)
    
    def _matches_filters(self, record: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if a record matches the given filters."""
        if not filters:
            return True
        
        for key, value in filters.items():
            if key not in record or record[key] != value:
                return False
        return True
    
    # User operations
    async def create_user(self, user: User) -> User:
        """Create a new user."""
        if not user.id:
            user.id = str(uuid.uuid4())
        
        user.created_at = datetime.datetime.now()
        user.updated_at = datetime.datetime.now()
        
        self.users[user.id] = user
        self.user_by_username[user.username] = user
        return user
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return self.user_by_username.get(username)
    
    async def update_user(self, user_id: str, data: Dict[str, Any]) -> Optional[User]:
        """Update a user."""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.datetime.now()
        return user
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        if user_id in self.users:
            user = self.users[user_id]
            del self.users[user_id]
            del self.user_by_username[user.username]
            return True
        return False
    
    # Chat operations
    async def create_chat(self, chat: Chat) -> Chat:
        """Create a new chat."""
        if not chat.id:
            chat.id = str(uuid.uuid4())
        
        chat.created_at = datetime.datetime.now()
        chat.updated_at = datetime.datetime.now()
        
        self.chats[chat.id] = chat
        return chat
    
    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        """Get a chat by ID."""
        return self.chats.get(chat_id)
    
    async def update_chat(self, chat_id: str, data: Dict[str, Any]) -> Optional[Chat]:
        """Update a chat."""
        if chat_id not in self.chats:
            return None
        
        chat = self.chats[chat_id]
        for key, value in data.items():
            if hasattr(chat, key):
                if key == "members" and isinstance(value, list):
                    # Handle members list specially
                    chat.members = [
                        UserInChat(**member) if isinstance(member, dict) else member
                        for member in value
                    ]
                else:
                    setattr(chat, key, value)
        
        chat.updated_at = datetime.datetime.now()
        return chat
    
    async def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat."""
        if chat_id in self.chats:
            del self.chats[chat_id]
            return True
        return False
    
    async def get_user_chats(self, user_id: str, 
                             skip: int = 0, limit: int = 100) -> List[Chat]:
        """Get all chats for a user."""
        user_chats = []
        for chat in self.chats.values():
            if chat.is_member(user_id):
                user_chats.append(chat)
        
        return user_chats[skip:skip + limit]
    
    async def add_chat_member(self, chat_id: str, user_id: str, role: str) -> bool:
        """Add a member to a chat."""
        if chat_id not in self.chats:
            return False
        
        chat = self.chats[chat_id]
        if not chat.is_member(user_id):
            chat.add_member(user_id, UserRole(role))
        
        return True
    
    async def remove_chat_member(self, chat_id: str, user_id: str) -> bool:
        """Remove a member from a chat."""
        if chat_id not in self.chats:
            return False
        
        chat = self.chats[chat_id]
        chat.remove_member(user_id)
        return True
    
    async def get_chat_members(self, chat_id: str) -> List[Dict[str, Any]]:
        """Get all members of a chat."""
        if chat_id not in self.chats:
            return []
        
        chat = self.chats[chat_id]
        return [member.dict() for member in chat.members]
    
    # Message operations
    async def create_message(self, message: Message) -> Message:
        """Create a new message."""
        if not message.id:
            message.id = str(uuid.uuid4())
        
        message.created_at = datetime.datetime.now()
        message.updated_at = datetime.datetime.now()
        
        self.messages[message.id] = message
        return message
    
    async def get_message(self, message_id: str) -> Optional[Message]:
        """Get a message by ID."""
        return self.messages.get(message_id)
    
    async def update_message(self, message_id: str, data: Dict[str, Any]) -> Optional[Message]:
        """Update a message."""
        if message_id not in self.messages:
            return None
        
        message = self.messages[message_id]
        for key, value in data.items():
            if hasattr(message, key):
                setattr(message, key, value)
        
        message.updated_at = datetime.datetime.now()
        return message
    
    async def delete_message(self, message_id: str, delete_for_everyone: bool = False) -> bool:
        """Delete a message."""
        if message_id in self.messages:
            if delete_for_everyone:
                del self.messages[message_id]
            else:
                self.messages[message_id].is_deleted = True
            return True
        return False
    
    async def get_chat_messages(self, chat_id: str, 
                               before_id: Optional[str] = None,
                               after_id: Optional[str] = None,
                               skip: int = 0, limit: int = 50) -> List[Message]:
        """Get messages for a chat with pagination."""
        chat_messages = []
        for message in self.messages.values():
            if message.chat_id == chat_id and not message.is_deleted:
                chat_messages.append(message)
        
        # Sort by creation time
        chat_messages.sort(key=lambda m: m.created_at, reverse=True)
        
        return chat_messages[skip:skip + limit]
    
    async def get_message_count(self, chat_id: str, since: Optional[str] = None) -> int:
        """Get the number of messages in a chat since a specific time."""
        count = 0
        for message in self.messages.values():
            if message.chat_id == chat_id and not message.is_deleted:
                count += 1
        return count
    
    # Reaction operations
    async def add_reaction(self, message_id: str, user_id: str, reaction_type: str) -> Optional[Reaction]:
        """Add a reaction to a message."""
        if message_id not in self.messages:
            return None
        
        message = self.messages[message_id]
        
        # Check if user already reacted with this type
        for reaction in message.reactions:
            if reaction.user_id == user_id and reaction.reaction_type == reaction_type:
                return reaction
        
        # Create new reaction
        reaction = Reaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            reaction_type=reaction_type,
            created_at=datetime.datetime.now()
        )
        
        message.reactions.append(reaction)
        return reaction
    
    async def remove_reaction(self, message_id: str, user_id: str, reaction_type: str) -> bool:
        """Remove a reaction from a message."""
        if message_id not in self.messages:
            return False
        
        message = self.messages[message_id]
        
        # Find and remove reaction
        for i, reaction in enumerate(message.reactions):
            if reaction.user_id == user_id and reaction.reaction_type == reaction_type:
                del message.reactions[i]
                return True
        
        return False
    
    async def get_message_reactions(self, message_id: str) -> List[Reaction]:
        """Get all reactions for a message."""
        if message_id not in self.messages:
            return []
        
        return self.messages[message_id].reactions
    
    # Search operations
    async def search_messages(self, query: str, user_id: str, 
                             chat_id: Optional[str] = None,
                             skip: int = 0, limit: int = 20) -> List[Message]:
        """Search for messages."""
        results = []
        
        for message in self.messages.values():
            if query.lower() in message.content.lower():
                if chat_id is None or message.chat_id == chat_id:
                    # Check if user has access to this message
                    if message.chat_id in self.chats:
                        chat = self.chats[message.chat_id]
                        if chat.is_member(user_id):
                            results.append(message)
        
        return results[skip:skip + limit]
    
    # Stats and aggregation
    async def get_chat_stats(self, chat_id: str) -> Dict[str, Any]:
        """Get statistics for a chat."""
        message_count = 0
        for message in self.messages.values():
            if message.chat_id == chat_id:
                message_count += 1
        
        return {
            "chat_id": chat_id,
            "message_count": message_count,
            "member_count": len(self.chats.get(chat_id, Chat()).members) if chat_id in self.chats else 0
        }
    
    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics for a user."""
        message_count = 0
        for message in self.messages.values():
            if message.sender_id == user_id:
                message_count += 1
        
        chat_count = 0
        for chat in self.chats.values():
            if chat.is_member(user_id):
                chat_count += 1
        
        return {
            "user_id": user_id,
            "message_count": message_count,
            "chat_count": chat_count
        }