"""
Database configuration and models using SQLModel.
Provides database connection and table definitions.
"""

import os
from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional, Generator
from datetime import datetime
from enum import Enum


class NodeType(str, Enum):
    """Node type enumeration for database."""
    ROOT = "root"
    BRANCH = "branch"
    LEAF = "leaf"


class Node(SQLModel, table=True):
    """Node table model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: Optional[str] = Field(default=None, max_length=1000)
    node_type: NodeType = Field(default=NodeType.LEAF)
    parent_id: Optional[int] = Field(default=None, foreign_key="node.id")
    position_x: Optional[float] = Field(default=None)
    position_y: Optional[float] = Field(default=None)
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color
    tags: Optional[str] = Field(default=None)  # JSON string of tags
    node_metadata: Optional[str] = Field(default=None)  # JSON string of metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class NodeConnection(SQLModel, table=True):
    """Node connections table model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    source_node_id: int = Field(foreign_key="node.id")
    target_node_id: int = Field(foreign_key="node.id")
    connection_type: str = Field(default="related", max_length=50)
    weight: Optional[float] = Field(default=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mindmap.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=os.getenv("DEBUG", "false").lower() == "true"
)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(engine) as session:
        yield session


def init_db():
    """Initialize database with tables."""
    create_db_and_tables()
    print("✅ Database tables created")


# Database utility functions
def get_session() -> Session:
    """Get a database session."""
    return Session(engine)
