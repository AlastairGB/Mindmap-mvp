"""
Mind Map Service
Business logic for mind map operations.
Handles CRUD operations, node relationships, and data management.
"""

import json
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, and_, or_
from datetime import datetime

from models.database import Node, NodeConnection
from models.node import NodeCreate, NodeUpdate, NodeResponse, NodeType


class MindMapService:
    """Service class for mind map operations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
    
    async def create_node(self, node_data: NodeCreate) -> NodeResponse:
        """Create a new node."""
        # Convert tags and metadata to JSON strings for storage
        tags_json = json.dumps(node_data.tags) if node_data.tags else None
        metadata_json = json.dumps(node_data.metadata) if node_data.metadata else None
        
        # Create node instance
        db_node = Node(
            title=node_data.title,
            content=node_data.content,
            node_type=node_data.node_type,
            parent_id=node_data.parent_id,
            position_x=node_data.position_x,
            position_y=node_data.position_y,
            color=node_data.color,
            tags=tags_json,
            node_metadata=metadata_json
        )
        
        # Add to database
        self.db.add(db_node)
        self.db.commit()
        self.db.refresh(db_node)
        
        # Convert to response model
        return await self._node_to_response(db_node)
    
    async def get_node(self, node_id: int) -> Optional[NodeResponse]:
        """Get a node by ID."""
        statement = select(Node).where(Node.id == node_id)
        db_node = self.db.exec(statement).first()
        
        if not db_node:
            return None
        
        return await self._node_to_response(db_node)
    
    async def list_nodes(self, skip: int = 0, limit: int = 100) -> List[NodeResponse]:
        """List nodes with pagination."""
        statement = select(Node).offset(skip).limit(limit)
        db_nodes = self.db.exec(statement).all()
        
        return [await self._node_to_response(node) for node in db_nodes]
    
    async def update_node(self, node_id: int, node_update: NodeUpdate) -> Optional[NodeResponse]:
        """Update an existing node."""
        statement = select(Node).where(Node.id == node_id)
        db_node = self.db.exec(statement).first()
        
        if not db_node:
            return None
        
        # Update fields if provided
        update_data = node_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "tags" and value is not None:
                setattr(db_node, field, json.dumps(value))
            elif field == "metadata" and value is not None:
                setattr(db_node, field, json.dumps(value))
            else:
                setattr(db_node, field, value)
        
        # Update timestamp
        db_node.updated_at = datetime.utcnow()
        
        self.db.add(db_node)
        self.db.commit()
        self.db.refresh(db_node)
        
        return await self._node_to_response(db_node)
    
    async def delete_node(self, node_id: int) -> bool:
        """Delete a node."""
        statement = select(Node).where(Node.id == node_id)
        db_node = self.db.exec(statement).first()
        
        if not db_node:
            return False
        
        # Delete all connections involving this node
        self.db.exec(select(NodeConnection).where(
            or_(
                NodeConnection.source_node_id == node_id,
                NodeConnection.target_node_id == node_id
            )
        ))
        
        # Delete the node
        self.db.delete(db_node)
        self.db.commit()
        
        return True
    
    async def link_nodes(self, source_id: int, target_id: int) -> bool:
        """Create a link between two nodes."""
        # Check if nodes exist
        source_node = self.db.exec(select(Node).where(Node.id == source_id)).first()
        target_node = self.db.exec(select(Node).where(Node.id == target_id)).first()
        
        if not source_node or not target_node:
            return False
        
        # Check if connection already exists
        existing = self.db.exec(select(NodeConnection).where(
            and_(
                NodeConnection.source_node_id == source_id,
                NodeConnection.target_node_id == target_id
            )
        )).first()
        
        if existing:
            return True  # Connection already exists
        
        # Create connection
        connection = NodeConnection(
            source_node_id=source_id,
            target_node_id=target_id
        )
        
        self.db.add(connection)
        self.db.commit()
        
        return True
    
    async def unlink_nodes(self, source_id: int, target_id: int) -> bool:
        """Remove a link between two nodes."""
        statement = select(NodeConnection).where(
            and_(
                NodeConnection.source_node_id == source_id,
                NodeConnection.target_node_id == target_id
            )
        )
        connection = self.db.exec(statement).first()
        
        if not connection:
            return False
        
        self.db.delete(connection)
        self.db.commit()
        
        return True
    
    async def get_node_connections(self, node_id: int) -> List[Dict[str, Any]]:
        """Get all connections for a node."""
        # Get outgoing connections
        outgoing = self.db.exec(select(NodeConnection).where(
            NodeConnection.source_node_id == node_id
        )).all()
        
        # Get incoming connections
        incoming = self.db.exec(select(NodeConnection).where(
            NodeConnection.target_node_id == node_id
        )).all()
        
        connections = []
        
        for conn in outgoing:
            target_node = self.db.exec(select(Node).where(Node.id == conn.target_node_id)).first()
            if target_node:
                connections.append({
                    "id": conn.id,
                    "target_node": {
                        "id": target_node.id,
                        "title": target_node.title,
                        "node_type": target_node.node_type
                    },
                    "direction": "outgoing",
                    "connection_type": conn.connection_type,
                    "weight": conn.weight
                })
        
        for conn in incoming:
            source_node = self.db.exec(select(Node).where(Node.id == conn.source_node_id)).first()
            if source_node:
                connections.append({
                    "id": conn.id,
                    "source_node": {
                        "id": source_node.id,
                        "title": source_node.title,
                        "node_type": source_node.node_type
                    },
                    "direction": "incoming",
                    "connection_type": conn.connection_type,
                    "weight": conn.weight
                })
        
        return connections
    
    async def save_mindmap_to_db(self, mindmap_data: Dict[str, Any]) -> List[NodeResponse]:
        """Save AI-generated mind map data to database."""
        saved_nodes = []
        
        # Create root node
        root_node_data = NodeCreate(
            title=mindmap_data.get("root", "Mind Map"),
            node_type=NodeType.ROOT,
            content="AI-generated mind map"
        )
        root_node = await self.create_node(root_node_data)
        saved_nodes.append(root_node)
        
        # Create child nodes
        children = mindmap_data.get("children", [])
        for child_data in children:
            child_node_data = NodeCreate(
                title=child_data.get("node", "Untitled"),
                node_type=NodeType.BRANCH,
                parent_id=root_node.id,
                content=f"Cluster with {len(child_data.get('children', []))} items"
            )
            child_node = await self.create_node(child_node_data)
            saved_nodes.append(child_node)
            
            # Create leaf nodes for children
            for item in child_data.get("children", []):
                leaf_node_data = NodeCreate(
                    title=str(item)[:100],  # Truncate if too long
                    node_type=NodeType.LEAF,
                    parent_id=child_node.id,
                    content=str(item)
                )
                leaf_node = await self.create_node(leaf_node_data)
                saved_nodes.append(leaf_node)
        
        return saved_nodes
    
    async def export_mindmap_json(self) -> Dict[str, Any]:
        """Export mind map as JSON structure."""
        # Get all nodes
        all_nodes = self.db.exec(select(Node)).all()
        
        # Build hierarchical structure
        nodes_by_id = {node.id: node for node in all_nodes}
        root_nodes = [node for node in all_nodes if node.parent_id is None]
        
        def build_node_tree(node):
            children = [n for n in all_nodes if n.parent_id == node.id]
            return {
                "id": node.id,
                "title": node.title,
                "content": node.content,
                "node_type": node.node_type,
                "position": {"x": node.position_x, "y": node.position_y},
                "color": node.color,
                "children": [build_node_tree(child) for child in children]
            }
        
        if root_nodes:
            return {
                "root": root_nodes[0].title,
                "children": [build_node_tree(node) for node in root_nodes],
                "total_nodes": len(all_nodes),
                "exported_at": datetime.utcnow().isoformat()
            }
        else:
            return {
                "root": "Empty Mind Map",
                "children": [],
                "total_nodes": 0,
                "exported_at": datetime.utcnow().isoformat()
            }
    
    async def _node_to_response(self, db_node: Node) -> NodeResponse:
        """Convert database node to response model."""
        # Parse JSON fields
        tags = json.loads(db_node.tags) if db_node.tags else None
        metadata = json.loads(db_node.node_metadata) if db_node.node_metadata else None
        
        # Count children
        children_count = len(self.db.exec(select(Node).where(Node.parent_id == db_node.id)).all())
        
        # Count connections
        connections_count = len(self.db.exec(select(NodeConnection).where(
            or_(
                NodeConnection.source_node_id == db_node.id,
                NodeConnection.target_node_id == db_node.id
            )
        )).all())
        
        return NodeResponse(
            id=db_node.id,
            title=db_node.title,
            content=db_node.content,
            node_type=db_node.node_type,
            parent_id=db_node.parent_id,
            position_x=db_node.position_x,
            position_y=db_node.position_y,
            color=db_node.color,
            tags=tags,
            metadata=metadata,
            created_at=db_node.created_at,
            updated_at=db_node.updated_at,
            children_count=children_count,
            connections_count=connections_count
        )
