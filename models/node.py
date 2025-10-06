"""
Node models for the Mind Map API
Defines Pydantic models for request/response and database models.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class NodeType(str, Enum):
    """Node type enumeration."""
    ROOT = "root"
    BRANCH = "branch"
    LEAF = "leaf"


class NodeCreate(BaseModel):
    """Model for creating a new node."""
    title: str = Field(..., min_length=1, max_length=200, description="Node title")
    content: Optional[str] = Field(None, max_length=1000, description="Node content/description")
    node_type: NodeType = Field(NodeType.LEAF, description="Type of node")
    parent_id: Optional[int] = Field(None, description="Parent node ID")
    position_x: Optional[float] = Field(None, description="X position in mind map")
    position_y: Optional[float] = Field(None, description="Y position in mind map")
    color: Optional[str] = Field(None, description="Node color (hex code)")
    tags: Optional[List[str]] = Field(None, description="Node tags")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class NodeUpdate(BaseModel):
    """Model for updating an existing node."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, max_length=1000)
    node_type: Optional[NodeType] = None
    parent_id: Optional[int] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    color: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class NodeResponse(BaseModel):
    """Model for node API responses."""
    id: int
    title: str
    content: Optional[str]
    node_type: NodeType
    parent_id: Optional[int]
    position_x: Optional[float]
    position_y: Optional[float]
    color: Optional[str]
    tags: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    children_count: int = 0
    connections_count: int = 0

    class Config:
        from_attributes = True


class NodeConnection(BaseModel):
    """Model for node connections."""
    id: int
    source_node_id: int
    target_node_id: int
    connection_type: str = "related"
    weight: Optional[float] = 1.0
    created_at: datetime

    class Config:
        from_attributes = True


class MindMapExport(BaseModel):
    """Model for exporting mind map data."""
    root: str = "Mind Map"
    children: List[Dict[str, Any]]
    total_nodes: int
    total_connections: int
    created_at: datetime
    updated_at: datetime
