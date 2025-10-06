#!/usr/bin/env python3
"""
Test client for Mind Map AI API
Demonstrates all API endpoints and functionality.
"""

import asyncio
import json
import httpx
from typing import Dict, Any, List
import time


class MindMapAPIClient:
    """Client for testing Mind Map AI API endpoints."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize API client."""
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def health_check(self) -> Dict[str, Any]:
        """Test health check endpoint."""
        print("🔍 Testing health check...")
        response = await self.client.get(f"{self.base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.json()
    
    async def create_node(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new node."""
        print(f"📝 Creating node: {node_data['title']}")
        response = await self.client.post(f"{self.base_url}/nodes", json=node_data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Created node ID: {result.get('id')}")
        return result
    
    async def get_node(self, node_id: int) -> Dict[str, Any]:
        """Get a specific node."""
        print(f"🔍 Getting node {node_id}...")
        response = await self.client.get(f"{self.base_url}/nodes/{node_id}")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Node title: {result.get('title')}")
        return result
    
    async def list_nodes(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """List all nodes."""
        print(f"📋 Listing nodes (skip={skip}, limit={limit})...")
        response = await self.client.get(f"{self.base_url}/nodes?skip={skip}&limit={limit}")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Found {len(result)} nodes")
        return result
    
    async def update_node(self, node_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a node."""
        print(f"✏️  Updating node {node_id}...")
        response = await self.client.put(f"{self.base_url}/nodes/{node_id}", json=update_data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Updated node title: {result.get('title')}")
        return result
    
    async def link_nodes(self, source_id: int, target_id: int) -> Dict[str, Any]:
        """Link two nodes."""
        print(f"🔗 Linking nodes {source_id} -> {target_id}...")
        response = await self.client.post(f"{self.base_url}/nodes/{source_id}/link/{target_id}")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Link result: {result.get('message')}")
        return result
    
    async def get_node_connections(self, node_id: int) -> Dict[str, Any]:
        """Get node connections."""
        print(f"🔗 Getting connections for node {node_id}...")
        response = await self.client.get(f"{self.base_url}/nodes/{node_id}/connections")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Found {len(result.get('connections', []))} connections")
        return result
    
    async def generate_mindmap(self, text: str) -> Dict[str, Any]:
        """Generate mind map from text using AI."""
        print(f"🤖 Generating mind map from text...")
        response = await self.client.post(
            f"{self.base_url}/ai/generate-mindmap",
            json={"text": text}
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Created {result.get('nodes_created', 0)} nodes")
        return result
    
    async def get_ai_status(self) -> Dict[str, Any]:
        """Get AI pipeline status."""
        print("🤖 Getting AI status...")
        response = await self.client.get(f"{self.base_url}/ai/status")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   AI Status: {result.get('status')}")
        return result
    
    async def export_mindmap(self) -> Dict[str, Any]:
        """Export mind map."""
        print("📤 Exporting mind map...")
        response = await self.client.get(f"{self.base_url}/export/mindmap")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Exported {result.get('total_nodes', 0)} nodes")
        return result
    
    async def delete_node(self, node_id: int) -> Dict[str, Any]:
        """Delete a node."""
        print(f"🗑️  Deleting node {node_id}...")
        response = await self.client.delete(f"{self.base_url}/nodes/{node_id}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Delete result: {result.get('message')}")
            return result
        return {}


async def run_comprehensive_test():
    """Run comprehensive API tests."""
    print("🚀 Starting Mind Map AI API Tests")
    print("=" * 50)
    
    client = MindMapAPIClient()
    
    try:
        # Test 1: Health Check
        print("\n1. HEALTH CHECK")
        print("-" * 20)
        await client.health_check()
        
        # Test 2: AI Status
        print("\n2. AI STATUS")
        print("-" * 20)
        await client.get_ai_status()
        
        # Test 3: Create Nodes
        print("\n3. CREATE NODES")
        print("-" * 20)
        
        # Create root node
        root_node = await client.create_node({
            "title": "My Mind Map",
            "content": "This is the root of my mind map",
            "node_type": "root",
            "color": "#FF6B6B"
        })
        root_id = root_node["id"]
        
        # Create branch nodes
        branch1 = await client.create_node({
            "title": "Marketing Strategy",
            "content": "All marketing related ideas",
            "node_type": "branch",
            "parent_id": root_id,
            "color": "#4ECDC4"
        })
        branch1_id = branch1["id"]
        
        branch2 = await client.create_node({
            "title": "Technical Implementation",
            "content": "Technical aspects and implementation",
            "node_type": "branch",
            "parent_id": root_id,
            "color": "#45B7D1"
        })
        branch2_id = branch2["id"]
        
        # Create leaf nodes
        leaf1 = await client.create_node({
            "title": "Social Media Campaign",
            "content": "Focus on TikTok and Instagram",
            "node_type": "leaf",
            "parent_id": branch1_id,
            "color": "#96CEB4"
        })
        leaf1_id = leaf1["id"]
        
        leaf2 = await client.create_node({
            "title": "Email Marketing",
            "content": "Automated email sequences",
            "node_type": "leaf",
            "parent_id": branch1_id,
            "color": "#96CEB4"
        })
        leaf2_id = leaf2["id"]
        
        # Test 4: List Nodes
        print("\n4. LIST NODES")
        print("-" * 20)
        nodes = await client.list_nodes()
        
        # Test 5: Update Node
        print("\n5. UPDATE NODE")
        print("-" * 20)
        await client.update_node(leaf1_id, {
            "title": "Social Media Campaign (Updated)",
            "content": "Updated: Focus on TikTok, Instagram, and LinkedIn"
        })
        
        # Test 6: Link Nodes
        print("\n6. LINK NODES")
        print("-" * 20)
        await client.link_nodes(branch1_id, branch2_id)
        await client.link_nodes(leaf1_id, leaf2_id)
        
        # Test 7: Get Connections
        print("\n7. GET CONNECTIONS")
        print("-" * 20)
        await client.get_node_connections(branch1_id)
        
        # Test 8: AI Mind Map Generation
        print("\n8. AI MIND MAP GENERATION")
        print("-" * 20)
        sample_text = """
        I need to plan my marketing strategy for the new product launch. 
        We should focus on social media marketing, especially TikTok and Instagram. 
        The budget needs to be allocated between paid ads and influencer partnerships. 
        I also want to consider email marketing campaigns and SEO optimization. 
        The target audience is millennials and Gen Z consumers.
        """
        ai_result = await client.generate_mindmap(sample_text)
        
        # Test 9: Export Mind Map
        print("\n9. EXPORT MIND MAP")
        print("-" * 20)
        export_data = await client.export_mindmap()
        
        # Test 10: Final Node List
        print("\n10. FINAL NODE LIST")
        print("-" * 20)
        final_nodes = await client.list_nodes()
        
        print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print(f"📊 Total nodes created: {len(final_nodes)}")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await client.close()


async def quick_test():
    """Run a quick test of basic functionality."""
    print("🚀 Quick API Test")
    print("=" * 30)
    
    client = MindMapAPIClient()
    
    try:
        # Health check
        await client.health_check()
        
        # Create a simple node
        node = await client.create_node({
            "title": "Test Node",
            "content": "This is a test node",
            "node_type": "leaf"
        })
        
        # Get the node
        await client.get_node(node["id"])
        
        # List nodes
        await client.list_nodes()
        
        print("\n✅ Quick test completed!")
        
    except Exception as e:
        print(f"\n❌ Quick test failed: {e}")
    
    finally:
        await client.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        asyncio.run(quick_test())
    else:
        asyncio.run(run_comprehensive_test())
