#!/usr/bin/env python3
"""
Integration test for the complete Mind Map AI system.
Tests both backend and frontend integration.
"""

import subprocess
import time
import requests
import json
import sys
import os
from pathlib import Path

def test_backend():
    """Test if the backend is running and responding."""
    print("🔍 Testing backend...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend is not responding: {e}")
        return False

def test_frontend():
    """Test if the frontend is running and responding."""
    print("🔍 Testing frontend...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend is not responding: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints."""
    print("🔍 Testing API endpoints...")
    
    endpoints = [
        ("/health", "Health check"),
        ("/ai/status", "AI status"),
        ("/nodes", "List nodes"),
    ]
    
    all_passed = True
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: Status {response.status_code}")
                all_passed = False
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: {e}")
            all_passed = False
    
    return all_passed

def test_ai_generation():
    """Test AI mind map generation."""
    print("🔍 Testing AI mind map generation...")
    
    test_text = "I need to plan my marketing strategy for the new product launch. We should focus on social media marketing, especially TikTok and Instagram."
    
    try:
        response = requests.post(
            "http://localhost:8000/ai/generate-mindmap",
            json={"text": test_text},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI generation successful: {data.get('nodes_created', 0)} nodes created")
            return True
        else:
            print(f"❌ AI generation failed: Status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AI generation error: {e}")
        return False

def start_backend():
    """Start the backend server."""
    print("🚀 Starting backend server...")
    backend_process = subprocess.Popen(
        ["python3", "start_server.py"],
        cwd=Path(__file__).parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for backend to start
    for i in range(30):
        if test_backend():
            print("✅ Backend started successfully")
            return backend_process
        time.sleep(1)
        print(f"⏳ Waiting for backend... ({i+1}/30)")
    
    print("❌ Backend failed to start")
    backend_process.terminate()
    return None

def start_frontend():
    """Start the frontend server."""
    print("🚀 Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=Path(__file__).parent / "frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for frontend to start
    for i in range(30):
        if test_frontend():
            print("✅ Frontend started successfully")
            return frontend_process
        time.sleep(1)
        print(f"⏳ Waiting for frontend... ({i+1}/30)")
    
    print("❌ Frontend failed to start")
    frontend_process.terminate()
    return None

def main():
    """Run the complete integration test."""
    print("🧪 Mind Map AI Integration Test")
    print("=" * 50)
    
    # Check if servers are already running
    backend_running = test_backend()
    frontend_running = test_frontend()
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend if not running
        if not backend_running:
            backend_process = start_backend()
            if not backend_process:
                print("❌ Failed to start backend")
                return False
        
        # Start frontend if not running
        if not frontend_running:
            frontend_process = start_frontend()
            if not frontend_process:
                print("❌ Failed to start frontend")
                return False
        
        # Run tests
        print("\n📋 Running integration tests...")
        print("-" * 30)
        
        tests = [
            ("Backend Health", test_backend),
            ("Frontend Accessibility", test_frontend),
            ("API Endpoints", test_api_endpoints),
            ("AI Generation", test_ai_generation),
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🔍 {test_name}...")
            result = test_func()
            results.append((test_name, result))
        
        # Summary
        print("\n📊 Test Results Summary")
        print("=" * 30)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
            if result:
                passed += 1
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! The Mind Map AI system is working correctly.")
            print("\n🌐 Access your application:")
            print("   Frontend: http://localhost:3000")
            print("   Backend API: http://localhost:8000")
            print("   API Docs: http://localhost:8000/docs")
            return True
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Please check the logs above.")
            return False
    
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    finally:
        # Clean up processes
        if backend_process:
            print("\n🛑 Stopping backend...")
            backend_process.terminate()
        
        if frontend_process:
            print("🛑 Stopping frontend...")
            frontend_process.terminate()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
