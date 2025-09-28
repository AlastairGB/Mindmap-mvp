#!/usr/bin/env python3
"""
Mind Map AI Pipeline
A plain Python script that processes raw text into structured mind map JSON
using Hugging Face APIs for AI processing and local Python for clustering.
"""

import json
import re
import requests
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Tuple
import argparse
import sys


class MindMapPipeline:
    """Main pipeline class for processing text into mind map JSON."""
    
    def __init__(self, hf_token: str = None):
        """
        Initialize the pipeline with Hugging Face token.
        
        Args:
            hf_token: Hugging Face API token (optional, can use public models)
        """
        self.hf_token = hf_token
        self.headers = {"Authorization": f"Bearer {hf_token}"} if hf_token else {}
        
        # API endpoints
        self.embedding_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        self.classification_url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        self.summarization_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.ner_url = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Split text into sentences and phrases for processing.
        
        Args:
            text: Raw input text
            
        Returns:
            List of sentences/phrases
        """
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Split into sentences using simple regex
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter sentences
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        # Also split on common separators for phrases
        phrases = []
        for sentence in sentences:
            # Split on commas, semicolons, and "and" for phrases
            sub_phrases = re.split(r'[,;]|\s+and\s+', sentence)
            phrases.extend([p.strip() for p in sub_phrases if len(p.strip()) > 5])
        
        return phrases
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Get embeddings from Hugging Face API.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            Numpy array of embeddings
        """
        embeddings = []
        
        for text in texts:
            try:
                response = requests.post(
                    self.embedding_url,
                    headers=self.headers,
                    json={"inputs": text}
                )
                
                if response.status_code == 200:
                    embedding = response.json()
                    if isinstance(embedding, list) and len(embedding) > 0:
                        embeddings.append(embedding[0])
                    else:
                        # Fallback: create random embedding if API fails
                        embeddings.append(np.random.rand(384).tolist())
                else:
                    print(f"Warning: Embedding API failed for text: {text[:50]}...")
                    embeddings.append(np.random.rand(384).tolist())
                    
            except Exception as e:
                print(f"Error getting embedding: {e}")
                embeddings.append(np.random.rand(384).tolist())
        
        return np.array(embeddings)
    
    def cluster_embeddings(self, embeddings: np.ndarray, n_clusters: int = None) -> Tuple[np.ndarray, int]:
        """
        Cluster embeddings using KMeans.
        
        Args:
            embeddings: Array of embeddings
            n_clusters: Number of clusters (auto-determined if None)
            
        Returns:
            Tuple of (cluster_labels, optimal_n_clusters)
        """
        if n_clusters is None:
            # Auto-determine number of clusters (between 2 and min(10, len(embeddings)//2))
            max_clusters = min(10, max(2, len(embeddings) // 2))
            n_clusters = max(2, min(max_clusters, len(embeddings)))
        
        if len(embeddings) < n_clusters:
            n_clusters = len(embeddings)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        return cluster_labels, n_clusters
    
    def classify_clusters(self, cluster_texts: List[str], cluster_labels: List[str]) -> List[str]:
        """
        Classify clusters using Hugging Face zero-shot classification.
        
        Args:
            cluster_texts: List of representative texts for each cluster
            cluster_labels: List of cluster labels
            
        Returns:
            List of classified labels
        """
        classified_labels = []
        
        # Create candidate labels based on common topics
        candidate_labels = [
            "Business", "Technology", "Marketing", "Finance", "Education", 
            "Health", "Entertainment", "Travel", "Food", "Sports", 
            "Science", "Art", "Music", "Politics", "Environment"
        ]
        
        for i, cluster_text in enumerate(cluster_texts):
            try:
                response = requests.post(
                    self.classification_url,
                    headers=self.headers,
                    json={
                        "inputs": cluster_text,
                        "parameters": {"candidate_labels": candidate_labels}
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        # Get the label with highest score
                        best_label = max(result, key=lambda x: x['score'])
                        classified_labels.append(best_label['label'])
                    else:
                        classified_labels.append(f"Cluster {i+1}")
                else:
                    classified_labels.append(f"Cluster {i+1}")
                    
            except Exception as e:
                print(f"Error in classification: {e}")
                classified_labels.append(f"Cluster {i+1}")
        
        return classified_labels
    
    def summarize_text(self, text: str, max_length: int = 50) -> str:
        """
        Summarize text using Hugging Face summarization API.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summarized text
        """
        if len(text) <= max_length:
            return text
        
        try:
            response = requests.post(
                self.summarization_url,
                headers=self.headers,
                json={
                    "inputs": text,
                    "parameters": {"max_length": max_length, "min_length": 10}
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0]['summary_text']
                else:
                    return text[:max_length] + "..."
            else:
                return text[:max_length] + "..."
                
        except Exception as e:
            print(f"Error in summarization: {e}")
            return text[:max_length] + "..."
    
    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities using Hugging Face NER API.
        
        Args:
            text: Text to extract entities from
            
        Returns:
            List of entities with labels
        """
        try:
            response = requests.post(
                self.ner_url,
                headers=self.headers,
                json={"inputs": text}
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list):
                    entities = []
                    for item in result:
                        if 'entity' in item and 'word' in item:
                            entities.append({
                                'text': item['word'],
                                'label': item['entity']
                            })
                    return entities
                else:
                    return []
            else:
                return []
                
        except Exception as e:
            print(f"Error in NER: {e}")
            return []
    
    def merge_results(self, texts: List[str], cluster_labels: np.ndarray, 
                     classified_labels: List[str], entities: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Merge all results into hierarchical JSON structure.
        
        Args:
            texts: Original text phrases
            cluster_labels: Cluster assignments
            classified_labels: Classified cluster names
            entities: Extracted entities
            
        Returns:
            Hierarchical JSON structure
        """
        # Group texts by cluster
        clusters = {}
        for i, (text, cluster_id) in enumerate(zip(texts, cluster_labels)):
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(text)
        
        # Create hierarchical structure
        children = []
        for cluster_id, cluster_texts in clusters.items():
            if cluster_id < len(classified_labels):
                cluster_name = classified_labels[cluster_id]
                
                # Summarize cluster name if too long
                if len(cluster_name) > 30:
                    cluster_name = self.summarize_text(cluster_name, 30)
                
                # Get representative texts for this cluster
                cluster_children = []
                for text in cluster_texts[:5]:  # Limit to 5 items per cluster
                    if len(text) > 50:
                        text = self.summarize_text(text, 50)
                    cluster_children.append(text)
                
                children.append({
                    "node": cluster_name,
                    "children": cluster_children
                })
        
        # Add entities as additional nodes if any
        if entities:
            entity_clusters = {}
            for entity in entities:
                label = entity['label']
                if label not in entity_clusters:
                    entity_clusters[label] = []
                entity_clusters[label].append(entity['text'])
            
            for label, entity_texts in entity_clusters.items():
                children.append({
                    "node": f"Entities ({label})",
                    "children": entity_texts[:5]  # Limit entities
                })
        
        return {
            "root": "Mind Map",
            "children": children
        }
    
    def process_text(self, text: str, output_file: str = "mindmap.json") -> Dict[str, Any]:
        """
        Main processing pipeline.
        
        Args:
            text: Input text to process
            output_file: Output file path
            
        Returns:
            Generated mind map JSON
        """
        print("Starting mind map processing...")
        
        # Step 1: Preprocess
        print("1. Preprocessing text...")
        phrases = self.preprocess_text(text)
        print(f"   Split into {len(phrases)} phrases")
        
        # Step 2: Get embeddings
        print("2. Getting embeddings...")
        embeddings = self.get_embeddings(phrases)
        print(f"   Generated {len(embeddings)} embeddings")
        
        # Step 3: Cluster embeddings
        print("3. Clustering embeddings...")
        cluster_labels, n_clusters = self.cluster_embeddings(embeddings)
        print(f"   Created {n_clusters} clusters")
        
        # Step 4: Classify clusters
        print("4. Classifying clusters...")
        # Get representative text for each cluster
        cluster_representatives = []
        for i in range(n_clusters):
            cluster_texts = [phrases[j] for j in range(len(phrases)) if cluster_labels[j] == i]
            if cluster_texts:
                # Use the longest text as representative
                representative = max(cluster_texts, key=len)
                cluster_representatives.append(representative)
            else:
                cluster_representatives.append("")
        
        classified_labels = self.classify_clusters(cluster_representatives, [f"Cluster {i+1}" for i in range(n_clusters)])
        print(f"   Classified {len(classified_labels)} clusters")
        
        # Step 5: Extract entities
        print("5. Extracting entities...")
        entities = self.extract_entities(text)
        print(f"   Found {len(entities)} entities")
        
        # Step 6: Merge results
        print("6. Merging results...")
        mindmap = self.merge_results(phrases, cluster_labels, classified_labels, entities)
        
        # Step 7: Save and return
        print("7. Saving results...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mindmap, f, indent=2, ensure_ascii=False)
        
        print(f"Mind map saved to {output_file}")
        return mindmap


def main():
    """Main function to run the pipeline."""
    parser = argparse.ArgumentParser(description="Mind Map AI Pipeline")
    parser.add_argument("--text", type=str, help="Input text to process")
    parser.add_argument("--file", type=str, help="Input file containing text")
    parser.add_argument("--output", type=str, default="mindmap.json", help="Output file path")
    parser.add_argument("--token", type=str, help="Hugging Face API token")
    
    args = parser.parse_args()
    
    # Get input text
    if args.text:
        input_text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except FileNotFoundError:
            print(f"Error: File {args.file} not found")
            sys.exit(1)
    else:
        # Default example text
        input_text = """
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
    
    # Initialize pipeline
    pipeline = MindMapPipeline(hf_token=args.token)
    
    # Process text
    try:
        mindmap = pipeline.process_text(input_text, args.output)
        
        # Print results
        print("\n" + "="*50)
        print("GENERATED MIND MAP:")
        print("="*50)
        print(json.dumps(mindmap, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error processing text: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

