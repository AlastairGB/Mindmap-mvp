#!/usr/bin/env python3
"""
Test script for the Mind Map AI Pipeline
Demonstrates the pipeline with sample data and shows expected output format.
"""

import json
from mindmap_pipeline import MindMapPipeline

def test_pipeline():
    """Test the pipeline with sample data."""
    
    # Sample text for testing
    sample_text = """
    I need to plan my marketing strategy for the new product launch. 
    We should focus on social media marketing, especially TikTok and Instagram. 
    The budget needs to be allocated between paid ads and influencer partnerships. 
    I also want to consider email marketing campaigns and SEO optimization. 
    The target audience is millennials and Gen Z consumers. 
    We need to track metrics like engagement rates, conversion rates, and ROI. 
    The launch date is set for next quarter, so we have time to prepare. 
    I should also research competitor strategies and market trends. 
    The product features include AI integration and mobile-first design. 
    Customer feedback from beta testing was very positive.
    """
    
    print("Testing Mind Map AI Pipeline...")
    print("="*50)
    
    # Initialize pipeline (without HF token for demo)
    pipeline = MindMapPipeline()
    
    # Process the text
    try:
        mindmap = pipeline.process_text(sample_text, "test_mindmap.json")
        
        print("\nPipeline completed successfully!")
        print(f"Generated mind map with {len(mindmap['children'])} main clusters")
        
        # Show structure
        print("\nMind Map Structure:")
        for i, cluster in enumerate(mindmap['children'], 1):
            print(f"  {i}. {cluster['node']} ({len(cluster['children'])} items)")
            for child in cluster['children'][:3]:  # Show first 3 items
                print(f"     - {child}")
            if len(cluster['children']) > 3:
                print(f"     ... and {len(cluster['children']) - 3} more")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_pipeline()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")

