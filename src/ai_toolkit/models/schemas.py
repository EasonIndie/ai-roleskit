"""
Data models and schemas for AI Character Toolkit.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
import uuid


class CharacterType(Enum):
    """Character types supported by the toolkit."""
    USER = "user"
    EXPERT = "expert"
    ORGANIZATION = "organization"


class DialogueRole(Enum):
    """Dialogue roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(Enum):
    """Message types in dialogue."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    FILE = "file"


@dataclass
class CharacterInfo:
    """Basic character information."""
    name: str
    age: Optional[str] = None
    position: Optional[str] = None
    background: Optional[str] = None
    experience: Optional[str] = None


@dataclass
class CharacterContext:
    """Character context and situation."""
    current_situation: Optional[str] = None
    goals: Optional[str] = None
    challenges: Optional[str] = None
    resource_constraints: Optional[str] = None


@dataclass
class CharacterExpertise:
    """Character expertise and skills."""
    professional_field: Optional[str] = None
    special_skills: Optional[str] = None
    experience_level: Optional[str] = None
    industry_insights: Optional[str] = None


@dataclass
class CharacterBehavior:
    """Character behavioral traits."""
    decision_style: Optional[str] = None
    risk_preference: Optional[str] = None
    communication_style: Optional[str] = None
    values: Optional[str] = None


@dataclass
class CharacterResponse:
    """Character response guidelines."""
    focus_areas: Optional[str] = None
    avoidance_areas: Optional[str] = None
    expression_style: Optional[str] = None
    expected_outcomes: Optional[str] = None


@dataclass
class Character:
    """AI Character definition."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: CharacterType = CharacterType.USER
    description: str = ""

    # Character components
    info: CharacterInfo = field(default_factory=CharacterInfo)
    context: CharacterContext = field(default_factory=CharacterContext)
    expertise: CharacterExpertise = field(default_factory=CharacterExpertise)
    behavior: CharacterBehavior = field(default_factory=CharacterBehavior)
    response: CharacterResponse = field(default_factory=CharacterResponse)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'description': self.description,
            'info': {
                'name': self.info.name,
                'age': self.info.age,
                'position': self.info.position,
                'background': self.info.background,
                'experience': self.info.experience
            },
            'context': {
                'current_situation': self.context.current_situation,
                'goals': self.context.goals,
                'challenges': self.context.challenges,
                'resource_constraints': self.context.resource_constraints
            },
            'expertise': {
                'professional_field': self.expertise.professional_field,
                'special_skills': self.expertise.special_skills,
                'experience_level': self.expertise.experience_level,
                'industry_insights': self.expertise.industry_insights
            },
            'behavior': {
                'decision_style': self.behavior.decision_style,
                'risk_preference': self.behavior.risk_preference,
                'communication_style': self.behavior.communication_style,
                'values': self.behavior.values
            },
            'response': {
                'focus_areas': self.response.focus_areas,
                'avoidance_areas': self.response.avoidance_areas,
                'expression_style': self.response.expression_style,
                'expected_outcomes': self.response.expected_outcomes
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tags': self.tags,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create character from dictionary."""
        character = cls()
        character.id = data.get('id', str(uuid.uuid4()))
        character.name = data.get('name', '')
        character.type = CharacterType(data.get('type', CharacterType.USER.value))
        character.description = data.get('description', '')

        # Load character components
        if 'info' in data:
            character.info = CharacterInfo(**data['info'])
        if 'context' in data:
            character.context = CharacterContext(**data['context'])
        if 'expertise' in data:
            character.expertise = CharacterExpertise(**data['expertise'])
        if 'behavior' in data:
            character.behavior = CharacterBehavior(**data['behavior'])
        if 'response' in data:
            character.response = CharacterResponse(**data['response'])

        # Load metadata
        character.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        character.updated_at = datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        character.tags = data.get('tags', [])
        character.metadata = data.get('metadata', {})

        return character


@dataclass
class Message:
    """Dialogue message."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: DialogueRole = DialogueRole.USER
    content: str = ""
    message_type: MessageType = MessageType.TEXT
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'id': self.id,
            'role': self.role.value,
            'content': self.content,
            'message_type': self.message_type.value,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary."""
        message = cls()
        message.id = data.get('id', str(uuid.uuid4()))
        message.role = DialogueRole(data.get('role', DialogueRole.USER.value))
        message.content = data.get('content', '')
        message.message_type = MessageType(data.get('message_type', MessageType.TEXT.value))
        message.timestamp = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
        message.metadata = data.get('metadata', {})
        return message


@dataclass
class Dialogue:
    """Dialogue session."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    character_id: str = ""
    title: str = ""
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, message: Message):
        """Add a message to the dialogue."""
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_last_messages(self, count: int = 10) -> List[Message]:
        """Get the last N messages."""
        return self.messages[-count:] if self.messages else []

    def to_dict(self) -> Dict[str, Any]:
        """Convert dialogue to dictionary."""
        return {
            'id': self.id,
            'character_id': self.character_id,
            'title': self.title,
            'messages': [msg.to_dict() for msg in self.messages],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dialogue':
        """Create dialogue from dictionary."""
        dialogue = cls()
        dialogue.id = data.get('id', str(uuid.uuid4()))
        dialogue.character_id = data.get('character_id', '')
        dialogue.title = data.get('title', '')
        dialogue.messages = [Message.from_dict(msg) for msg in data.get('messages', [])]
        dialogue.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        dialogue.updated_at = datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        dialogue.metadata = data.get('metadata', {})
        return dialogue


@dataclass
class ExplorationSession:
    """Creative exploration session."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    initial_idea: str = ""
    exploration_data: Dict[str, Any] = field(default_factory=dict)
    generated_characters: List[str] = field(default_factory=list)  # Character IDs
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def add_character(self, character_id: str):
        """Add a generated character ID."""
        if character_id not in self.generated_characters:
            self.generated_characters.append(character_id)
            self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert exploration session to dictionary."""
        return {
            'id': self.id,
            'initial_idea': self.initial_idea,
            'exploration_data': self.exploration_data,
            'generated_characters': self.generated_characters,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExplorationSession':
        """Create exploration session from dictionary."""
        session = cls()
        session.id = data.get('id', str(uuid.uuid4()))
        session.initial_idea = data.get('initial_idea', '')
        session.exploration_data = data.get('exploration_data', {})
        session.generated_characters = data.get('generated_characters', [])
        session.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        session.updated_at = datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        return session


@dataclass
class ValidationSession:
    """Concurrent validation session."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    question: str = ""
    character_responses: Dict[str, str] = field(default_factory=dict)  # character_id -> response
    analysis_result: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def add_response(self, character_id: str, response: str):
        """Add a character response."""
        self.character_responses[character_id] = response

    def to_dict(self) -> Dict[str, Any]:
        """Convert validation session to dictionary."""
        return {
            'id': self.id,
            'question': self.question,
            'character_responses': self.character_responses,
            'analysis_result': self.analysis_result,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationSession':
        """Create validation session from dictionary."""
        session = cls()
        session.id = data.get('id', str(uuid.uuid4()))
        session.question = data.get('question', '')
        session.character_responses = data.get('character_responses', {})
        session.analysis_result = data.get('analysis_result', {})
        session.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        return session