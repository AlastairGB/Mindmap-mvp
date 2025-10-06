#!/usr/bin/env python3
"""
Startup script for Mind Map AI API server.
Handles environment setup and server initialization.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Start the FastAPI server."""
    print("🚀 Starting Mind Map AI API Server")
    print("=" * 50)
    
    # Check if database file exists, if not create it
    db_path = "mindmap.db"
    if not os.path.exists(db_path):
        print("📁 Creating database...")
        from models.database import init_db
        init_db()
    
    # Start the server
    print("🌐 Starting server on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Alternative docs: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
