"""
AI Pipeline Service
Integrates the existing mind map AI pipeline with the FastAPI backend.
Handles text processing and AI-powered mind map generation.
"""

import json
import requests
import numpy as np
from typing import Dict, Any, List
from sklearn.cluster import KMeans
from datetime import datetime

from mindmap_pipeline import MindMapPipeline


class AIPipelineService:
    """Service for AI-powered mind map generation."""
    
    def __init__(self, hf_token: str = None):
        """Initialize AI pipeline service."""
        self.pipeline = MindMapPipeline(hf_token=hf_token)
    
    async def process_text_to_mindmap(self, text: str) -> Dict[str, Any]:
        """
        Process raw text into mind map structure using AI pipeline.
        
        Args:
            text: Raw input text to process
            
        Returns:
            Dictionary containing mind map structure
        """
        try:
            # Use the existing pipeline to process text
            mindmap_data = self.pipeline.process_text(text, output_file=None)
            
            # Ensure we have the expected structure
            if not isinstance(mindmap_data, dict):
                raise ValueError("Invalid mind map data structure")
            
            # Add metadata
            mindmap_data["generated_at"] = datetime.utcnow().isoformat()
            mindmap_data["source_text_length"] = len(text)
            mindmap_data["ai_processed"] = True
            
            return mindmap_data
            
        except Exception as e:
            # Fallback: create a simple mind map structure
            return self._create_fallback_mindmap(text)
    
    def _create_fallback_mindmap(self, text: str) -> Dict[str, Any]:
        """Create a fallback mind map when AI processing fails."""
        # Simple text splitting as fallback
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # Group sentences into clusters (simple approach)
        clusters = []
        chunk_size = max(1, len(sentences) // 3)  # Create 3 clusters
        
        for i in range(0, len(sentences), chunk_size):
            chunk = sentences[i:i + chunk_size]
            if chunk:
                clusters.append({
                    "node": f"Topic {len(clusters) + 1}",
                    "children": chunk[:5]  # Limit to 5 items per cluster
                })
        
        return {
            "root": "Mind Map",
            "children": clusters,
            "generated_at": datetime.utcnow().isoformat(),
            "source_text_length": len(text),
            "ai_processed": False,
            "fallback_mode": True
        }
    
    async def get_ai_status(self) -> Dict[str, Any]:
        """Get status of AI services."""
        return {
            "status": "operational",
            "models": {
                "embeddings": "sentence-transformers/all-MiniLM-L6-v2",
                "classification": "facebook/bart-large-mnli",
                "summarization": "facebook/bart-large-cnn",
                "ner": "dslim/bert-base-NER"
            },
            "api_endpoints": {
                "embeddings": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2",
                "classification": "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
                "summarization": "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
                "ner": "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
            },
            "last_updated": datetime.utcnow().isoformat()
        }
    
    async def test_ai_services(self) -> Dict[str, Any]:
        """Test AI services connectivity."""
        test_results = {}
        
        # Test each service with a simple request
        test_text = "This is a test for AI services."
        
        try:
            # Test embeddings
            embeddings = self.pipeline.get_embeddings([test_text])
            test_results["embeddings"] = {
                "status": "success",
                "embedding_dimension": len(embeddings[0]) if len(embeddings) > 0 else 0
            }
        except Exception as e:
            test_results["embeddings"] = {
                "status": "error",
                "error": str(e)
            }
        
        try:
            # Test classification
            classification = self.pipeline.classify_clusters([test_text], ["test"])
            test_results["classification"] = {
                "status": "success",
                "result": classification[0] if classification else "unknown"
            }
        except Exception as e:
            test_results["classification"] = {
                "status": "error",
                "error": str(e)
            }
        
        try:
            # Test summarization
            summary = self.pipeline.summarize_text(test_text, 20)
            test_results["summarization"] = {
                "status": "success",
                "summary": summary
            }
        except Exception as e:
            test_results["summarization"] = {
                "status": "error",
                "error": str(e)
            }
        
        try:
            # Test NER
            entities = self.pipeline.extract_entities(test_text)
            test_results["ner"] = {
                "status": "success",
                "entities_found": len(entities)
            }
        except Exception as e:
            test_results["ner"] = {
                "status": "error",
                "error": str(e)
            }
        
        return {
            "test_results": test_results,
            "overall_status": "operational" if all(
                result["status"] == "success" for result in test_results.values()
            ) else "degraded",
            "tested_at": datetime.utcnow().isoformat()
        }
