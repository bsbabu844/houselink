#!/usr/bin/env python3
"""
PolitiQ Phase I - Startup Script
Simple script to start the application with proper configuration
"""

import uvicorn
import sys
import os

def main():
    """Main startup function"""
    print("🚀 Starting PolitiQ Phase I - House-Level Voter Mapping Tool")
    print("=" * 60)
    print()
    
    # Check if app directory exists
    if not os.path.exists('app'):
        print("❌ Error: 'app' directory not found!")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import fastapi
        import sqlalchemy
        import pandas
        import pdfplumber
        print("✅ Dependencies check passed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    print("🔧 Configuration:")
    print("   - Host: 0.0.0.0")
    print("   - Port: 8000")
    print("   - Reload: True")
    print("   - Database: SQLite (politiq.db)")
    print()
    
    print("🌐 Access URLs:")
    print("   - Admin Dashboard: http://localhost:8000/")
    print("   - API Documentation: http://localhost:8000/docs")
    print("   - OpenAPI Spec: http://localhost:8000/openapi.json")
    print()
    
    print("📋 Quick Start:")
    print("   1. Import hierarchy data (Excel file)")
    print("   2. Create booths manually")
    print("   3. Upload voter PDFs")
    print("   4. Search and view voter data")
    print()
    
    print("🔄 Starting server...")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()