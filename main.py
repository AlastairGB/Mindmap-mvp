#!/usr/bin/env python3
"""
FastAPI Backend for Mind Map AI MVP
Main entry point for the API server.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
import os
from dotenv import load_dotenv

from models.database import get_db, init_db, Node
from models.node import NodeCreate, NodeUpdate, NodeResponse
from services.mindmap import MindMapService
from services.ai_pipeline import AIPipelineService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Mind Map AI API",
    description="Backend API for AI-powered mind map creation and management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    print("✅ Database initialized")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Mind Map AI API is running"}

# Node CRUD endpoints
@app.post("/nodes", response_model=NodeResponse)
async def create_node(node: NodeCreate, db=Depends(get_db)):
    """Create a new mind map node."""
    try:
        service = MindMapService(db)
        created_node = await service.create_node(node)
        return created_node
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/nodes/{node_id}", response_model=NodeResponse)
async def get_node(node_id: int, db=Depends(get_db)):
    """Get a specific node by ID."""
    try:
        service = MindMapService(db)
        node = await service.get_node(node_id)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
        return node
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nodes", response_model=List[NodeResponse])
async def list_nodes(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    """List all nodes with pagination."""
    try:
        service = MindMapService(db)
        nodes = await service.list_nodes(skip=skip, limit=limit)
        return nodes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/nodes/{node_id}", response_model=NodeResponse)
async def update_node(node_id: int, node_update: NodeUpdate, db=Depends(get_db)):
    """Update an existing node."""
    try:
        service = MindMapService(db)
        updated_node = await service.update_node(node_id, node_update)
        if not updated_node:
            raise HTTPException(status_code=404, detail="Node not found")
        return updated_node
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/nodes/{node_id}")
async def delete_node(node_id: int, db=Depends(get_db)):
    """Delete a node."""
    try:
        service = MindMapService(db)
        success = await service.delete_node(node_id)
        if not success:
            raise HTTPException(status_code=404, detail="Node not found")
        return {"message": "Node deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Pipeline endpoints
@app.post("/ai/generate-mindmap")
async def generate_mindmap_from_text(
    request: dict,
    db=Depends(get_db)
):
    """Generate a mind map from raw text using AI pipeline."""
    try:
        ai_service = AIPipelineService()
        text = request.get("text", "")
        mindmap_data = await ai_service.process_text_to_mindmap(text)
        
        # Save generated nodes to database
        service = MindMapService(db)
        saved_nodes = await service.save_mindmap_to_db(mindmap_data)
        
        return {
            "message": "Mind map generated successfully",
            "nodes_created": len(saved_nodes),
            "mindmap_data": mindmap_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai/status")
async def ai_status():
    """Check AI pipeline status."""
    return {
        "status": "operational",
        "models": {
            "embeddings": "sentence-transformers/all-MiniLM-L6-v2",
            "classification": "facebook/bart-large-mnli",
            "summarization": "facebook/bart-large-cnn",
            "ner": "dslim/bert-base-NER"
        }
    }

# Node relationship endpoints
@app.post("/nodes/{node_id}/link/{target_id}")
async def link_nodes(node_id: int, target_id: int, db=Depends(get_db)):
    """Create a link between two nodes."""
    try:
        service = MindMapService(db)
        success = await service.link_nodes(node_id, target_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to create link")
        return {"message": "Nodes linked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/nodes/{node_id}/unlink/{target_id}")
async def unlink_nodes(node_id: int, target_id: int, db=Depends(get_db)):
    """Remove a link between two nodes."""
    try:
        service = MindMapService(db)
        success = await service.unlink_nodes(node_id, target_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to remove link")
        return {"message": "Nodes unlinked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nodes/{node_id}/connections")
async def get_node_connections(node_id: int, db=Depends(get_db)):
    """Get all connections for a specific node."""
    try:
        service = MindMapService(db)
        connections = await service.get_node_connections(node_id)
        return {"connections": connections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Export endpoints
@app.get("/export/mindmap")
async def export_mindmap(format: str = "json", db=Depends(get_db)):
    """Export the entire mind map."""
    try:
        service = MindMapService(db)
        if format == "json":
            mindmap = await service.export_mindmap_json()
            return mindmap
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
